"""Local clinic service. Adapted scheduling/version/outbox rules from the portfolio's clinic demo."""
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3

from domain import DOCTORS, ROLES, TRANSITIONS, appointment_fields, identifier, minutes, patient_fields, text, version_matches

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


class Product:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / 'clinic.sqlite3'
        with self.connect() as db:
            db.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))
            if not db.execute("SELECT 1 FROM meta WHERE key='initialized'").fetchone():
                self.seed(db)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def seed(self, db):
        for table in ['encounters', 'appointments', 'patients', 'operations', 'audit', 'meta']:
            db.execute('DELETE FROM ' + table)
        fixture = json.loads((ROOT / 'fixtures/clinic.json').read_text(encoding='utf-8'))
        db.executemany('INSERT INTO meta VALUES(?,?)', [('initialized', 'yes'), ('role', 'reception')])
        for p in fixture['patients']:
            db.execute('INSERT INTO patients(id,name,dob,phone,sex,administrative_note,created_at) VALUES(?,?,?,?,?,?,?)', (p['id'], p['name'], p['dob'], p['phone'], p['sex'], p['administrative_note'], now()))
        for a in fixture['appointments']:
            db.execute('INSERT INTO appointments(id,patient_id,doctor_id,date,time,duration,reason,status) VALUES(?,?,?,?,?,?,?,?)', (a['id'], a['patient_id'], a['doctor_id'], date.today().isoformat(), a['time'], a['duration'], a['reason'], a['status']))
        for e in fixture['encounters']:
            db.execute('INSERT INTO encounters VALUES(?,?,?,?,?,?,?,?)', (e['id'], e['patient_id'], e['appointment_id'], e['summary'], e['assessment'], e['plan'], e['author'], (datetime.now(timezone.utc) - timedelta(days=e['days_ago'])).isoformat(timespec='seconds')))

    def role(self, db):
        return db.execute("SELECT value FROM meta WHERE key='role'").fetchone()[0]

    def state(self):
        with self.connect() as db:
            role = self.role(db)
            patients = [dict(x) for x in db.execute('SELECT * FROM patients ORDER BY name')]
            if role in ['doctor', 'admin']:
                for p in patients:
                    p['encounters'] = [dict(x) for x in db.execute('SELECT * FROM encounters WHERE patient_id=? ORDER BY created_at DESC,rowid DESC', (p['id'],))]
            appointments = [dict(x) for x in db.execute('SELECT a.*,p.name patient_name FROM appointments a JOIN patients p ON p.id=a.patient_id ORDER BY date,time,id')]
            audit = [dict(x) for x in db.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 30')]
        return {'role': role, 'roles': ROLES, 'doctors': DOCTORS, 'patients': patients, 'appointments': appointments, 'today': date.today().isoformat(), 'transitions': TRANSITIONS, 'audit': audit, 'updated_at': now(), 'clinic': 'Cedar Family Clinic'}

    def action(self, name, payload):
        if name == 'sync':
            operations = payload.get('operations')
            if not isinstance(operations, list) or len(operations) > 100:
                raise ValueError('Send up to 100 queued changes')
            results = []
            for operation in operations:
                op_id = operation.get('id', '') if isinstance(operation, dict) else ''
                try:
                    if not isinstance(operation, dict) or not isinstance(operation.get('payload'), dict):
                        raise ValueError('Invalid queued change')
                    if not op_id:
                        raise ValueError('Queued changes require a stable identifier')
                    identifier(op_id)
                    result = self.mutate(operation.get('name'), operation['payload'], op_id, operation.get('role'))
                    results.append({'id': op_id, 'status': 'synced', 'result': result})
                except (ValueError, RuntimeError, PermissionError) as error:
                    results.append({'id': op_id, 'status': 'conflict' if isinstance(error, RuntimeError) else 'denied' if isinstance(error, PermissionError) else 'invalid', 'error': str(error)})
            return {'results': results}
        if name in ['set_role', 'reset']:
            with self.connect() as db:
                if name == 'reset':
                    self.seed(db)
                else:
                    if payload.get('role') not in ROLES:
                        raise ValueError('Unknown staff role')
                    db.execute("UPDATE meta SET value=? WHERE key='role'", (payload['role'],))
            return self.state()
        if name == 'export_patient':
            state = self.state()
            p = next((x for x in state['patients'] if x['id'] == payload.get('id')), None)
            if not p:
                raise ValueError('Patient not found')
            return {'filename': f"{p['id']}-record.json", 'content': json.dumps({'patient': p, 'appointments': [x for x in state['appointments'] if x['patient_id'] == p['id']]}, indent=2), 'mime': 'application/json'}
        return self.mutate(name, payload, payload.get('operation_id'), payload.get('staff_role'))

    def record(self, db, table, record_id):
        row = db.execute('SELECT * FROM ' + table + ' WHERE id=?', (record_id,)).fetchone()
        if not row:
            raise ValueError('Record not found')
        return row

    def mutate(self, name, payload, operation_id=None, queued_role=None):
        if name not in ['create_patient', 'update_patient', 'archive_patient', 'create_appointment', 'set_status', 'save_encounter']:
            raise ValueError('Unknown clinic action')
        if operation_id:
            identifier(operation_id)
        with self.connect() as db:
            role = self.role(db)
            if queued_role and queued_role != role:
                raise PermissionError('Switch to the staff role used for this queued change')
            if operation_id:
                previous = db.execute('SELECT * FROM operations WHERE id=?', (operation_id,)).fetchone()
                if previous:
                    if previous['role'] != role:
                        raise PermissionError('This change belongs to another staff role')
                    return json.loads(previous['result'])
            if name in ['create_patient', 'update_patient']:
                fields = patient_fields(payload)
                record_id = identifier(payload.get('id'), 'p-')
                if name == 'create_patient':
                    if db.execute('SELECT 1 FROM patients WHERE id=?', (record_id,)).fetchone():
                        raise RuntimeError('Patient identifier already exists')
                    db.execute('INSERT INTO patients(id,name,dob,phone,sex,administrative_note,created_at) VALUES(?,?,?,?,?,?,?)', (record_id, *fields.values(), now()))
                    version = 1
                else:
                    row = self.record(db, 'patients', record_id)
                    version_matches(row, payload)
                    db.execute('UPDATE patients SET name=?,dob=?,phone=?,sex=?,administrative_note=?,version=version+1 WHERE id=?', (*fields.values(), record_id))
                    version = row['version'] + 1
                result = {'id': record_id, 'version': version}
            elif name == 'archive_patient':
                row = self.record(db, 'patients', payload.get('id'))
                version_matches(row, payload)
                if db.execute("SELECT 1 FROM appointments WHERE patient_id=? AND status IN ('scheduled','arrived','in_progress')", (row['id'],)).fetchone():
                    raise RuntimeError('Complete or cancel active appointments before archiving')
                db.execute('UPDATE patients SET archived=1,version=version+1 WHERE id=?', (row['id'],))
                result = {'id': row['id'], 'version': row['version'] + 1, 'archived': True}
            elif name == 'create_appointment':
                p = self.record(db, 'patients', payload.get('patient_id'))
                if p['archived']:
                    raise ValueError('Archived patients cannot be booked')
                fields = appointment_fields(payload)
                start = minutes(fields['time'])
                for a in db.execute("SELECT * FROM appointments WHERE doctor_id=? AND date=? AND status!='cancelled'", (fields['doctor_id'], fields['date'])):
                    other = minutes(a['time'])
                    if start < other + a['duration'] and other < start + fields['duration']:
                        raise RuntimeError('This doctor already has an appointment at that time')
                record_id = identifier(payload.get('id'), 'a-')
                if db.execute('SELECT 1 FROM appointments WHERE id=?', (record_id,)).fetchone():
                    raise RuntimeError('Appointment identifier already exists')
                db.execute('INSERT INTO appointments(id,patient_id,doctor_id,date,time,duration,reason,status) VALUES(?,?,?,?,?,?,?,?)', (record_id, p['id'], *fields.values(), 'scheduled'))
                result = {'id': record_id, 'version': 1}
            elif name == 'set_status':
                row = self.record(db, 'appointments', payload.get('id'))
                version_matches(row, payload)
                status = payload.get('status')
                if role == 'reception' and status in ['in_progress', 'completed']:
                    raise PermissionError('A doctor starts and completes the visit')
                if status not in TRANSITIONS[row['status']]:
                    raise ValueError('This appointment status transition is unavailable')
                db.execute('UPDATE appointments SET status=?,version=version+1 WHERE id=?', (status, row['id']))
                result = {'id': row['id'], 'status': status, 'version': row['version'] + 1}
            elif name == 'save_encounter':
                if role not in ['doctor', 'admin']:
                    raise PermissionError('Visit notes are available to doctors and administrators')
                p = self.record(db, 'patients', payload.get('patient_id'))
                version_matches(p, payload)
                if p['archived']:
                    raise ValueError('Archived records cannot receive a visit note')
                a = self.record(db, 'appointments', payload.get('appointment_id'))
                if a['patient_id'] != p['id'] or a['status'] != 'in_progress':
                    raise ValueError('Start this patient’s visit before writing the encounter')
                summary = text(payload.get('summary', ''), 'Visit summary', 1, 500)
                assessment = text(payload.get('assessment', ''), 'Assessment', 0, 2000)
                plan = text(payload.get('plan', ''), 'Plan', 0, 2000)
                author = next(x['name'] for x in DOCTORS if x['id'] == a['doctor_id'])
                record_id = identifier(payload.get('id'), 'e-')
                if db.execute('SELECT 1 FROM encounters WHERE id=?', (record_id,)).fetchone():
                    raise RuntimeError('Encounter identifier already exists')
                db.execute('INSERT INTO encounters VALUES(?,?,?,?,?,?,?,?)', (record_id, p['id'], a['id'], summary, assessment, plan, author, now()))
                db.execute('UPDATE patients SET version=version+1 WHERE id=?', (p['id'],))
                result = {'id': p['id'], 'encounter_id': record_id, 'version': p['version'] + 1}
            db.execute('INSERT INTO audit(action,record_id,role,created_at) VALUES(?,?,?,?)', (name, result['id'], role, now()))
            if operation_id:
                db.execute('INSERT INTO operations VALUES(?,?,?)', (operation_id, role, json.dumps(result)))
        return result
