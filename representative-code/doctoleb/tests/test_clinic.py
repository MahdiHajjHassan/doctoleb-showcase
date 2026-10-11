"""Persisted clinic contracts; run with python -m unittest discover -s tests -v."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ClinicTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'service.py').is_file(), 'The clinic service must exist')
        sys.path.insert(0, str(ROOT))
        from service import Product
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.product = Product(Path(self.temp.name))

    def patient(self):
        return self.product.action('create_patient', {'id': 'p-test-new', 'name': 'Rana Haddad', 'dob': '1990-05-12', 'phone': '+961 00 000 123'})

    def book(self, patient_id, time='16:00'):
        return self.product.action('create_appointment', {'id': 'a-test-new', 'patient_id': patient_id, 'doctor_id': 'doctor-1', 'date': self.product.state()['today'], 'time': time, 'duration': 30, 'reason': 'Follow-up'})

    def test_register_book_checkin_visit_and_reopen(self):
        p = self.patient()
        a = self.book(p['id'])
        self.product.action('set_status', {'id': a['id'], 'status': 'arrived', 'version': 1})
        self.product.action('set_role', {'role': 'doctor'})
        self.product.action('set_status', {'id': a['id'], 'status': 'in_progress', 'version': 2})
        note = self.product.action('save_encounter', {'patient_id': p['id'], 'appointment_id': a['id'], 'version': 1, 'summary': 'Follow-up completed', 'assessment': 'Reviewed progress', 'plan': 'Return in four weeks'})
        self.assertEqual(note['version'], 2)
        self.product.action('set_status', {'id': a['id'], 'status': 'completed', 'version': 3})
        from service import Product
        reopened = Product(Path(self.temp.name)).state()
        patient = next(x for x in reopened['patients'] if x['id'] == p['id'])
        self.assertEqual(patient['encounters'][0]['plan'], 'Return in four weeks')
        self.assertEqual(next(x for x in reopened['appointments'] if x['id'] == a['id'])['status'], 'completed')

    def test_reception_cannot_read_or_write_encounters(self):
        state = self.product.state()
        self.assertTrue(all('encounters' not in p for p in state['patients']))
        with self.assertRaises(PermissionError):
            self.product.action('save_encounter', {'patient_id': state['patients'][0]['id'], 'version': 1, 'summary': 'Restricted'})
        appointment = next(x for x in state['appointments'] if x['status'] == 'arrived')
        with self.assertRaises(PermissionError):
            self.product.action('set_status', {'id': appointment['id'], 'version': appointment['version'], 'status': 'in_progress'})

    def test_overlap_and_stale_edit_rejected_without_mutation(self):
        p = self.patient()
        a = self.book(p['id'])
        with self.assertRaises(RuntimeError):
            self.product.action('create_appointment', {'patient_id': p['id'], 'doctor_id': 'doctor-1', 'date': self.product.state()['today'], 'time': '16:15', 'duration': 30})
        with self.assertRaises(RuntimeError):
            self.product.action('set_status', {'id': a['id'], 'version': 0, 'status': 'arrived'})
        self.assertEqual(next(x for x in self.product.state()['appointments'] if x['id'] == a['id'])['version'], 1)

    def test_ordered_offline_batch_is_idempotent_and_role_bound(self):
        today = self.product.state()['today']
        operations = [
            {'id': 'op-patient-001', 'role': 'reception', 'name': 'create_patient', 'payload': {'id': 'p-offline-01', 'name': 'Offline patient'}},
            {'id': 'op-booking-001', 'role': 'reception', 'name': 'create_appointment', 'payload': {'id': 'a-offline-01', 'patient_id': 'p-offline-01', 'doctor_id': 'doctor-2', 'date': today, 'time': '17:00', 'duration': 30}},
            {'id': 'op-arrival-001', 'role': 'reception', 'name': 'set_status', 'payload': {'id': 'a-offline-01', 'version': 1, 'status': 'arrived'}},
        ]
        first = self.product.action('sync', {'operations': operations})
        second = self.product.action('sync', {'operations': operations})
        self.assertEqual(first, second)
        self.assertEqual([x['status'] for x in first['results']], ['synced'] * 3)
        self.assertEqual(sum(x['id'] == 'p-offline-01' for x in self.product.state()['patients']), 1)
        self.product.action('set_role', {'role': 'doctor'})
        denied = self.product.action('sync', {'operations': [{'id': 'op-denied-01', 'role': 'reception', 'name': 'create_patient', 'payload': {'name': 'Another patient'}}]})
        self.assertEqual(denied['results'][0]['status'], 'denied')

    def test_patient_update_archive_and_validation(self):
        p = self.patient()
        self.product.action('update_patient', {'id': p['id'], 'version': 1, 'name': 'Rana Haddad', 'phone': '+961 00 000 456', 'dob': '1990-05-12', 'sex': 'female', 'administrative_note': 'Prefers morning appointments'})
        patient = next(x for x in self.product.state()['patients'] if x['id'] == p['id'])
        self.assertEqual(patient['phone'], '+961 00 000 456')
        with self.assertRaises(RuntimeError):
            self.product.action('update_patient', {'id': p['id'], 'version': 1, 'name': 'Wrong stale name'})
        self.product.action('archive_patient', {'id': p['id'], 'version': 2})
        self.assertTrue(next(x for x in self.product.state()['patients'] if x['id'] == p['id'])['archived'])
        with self.assertRaises(ValueError):
            self.book(p['id'])
        with self.assertRaises(ValueError):
            self.product.action('create_patient', {'name': 'Future', 'dob': '2999-01-01'})

    def test_encounter_rejects_wrong_patient_and_requires_active_visit(self):
        state = self.product.state()
        appointment = state['appointments'][0]
        self.product.action('set_role', {'role': 'doctor'})
        with self.assertRaises(ValueError):
            self.product.action('save_encounter', {'patient_id': appointment['patient_id'], 'appointment_id': appointment['id'], 'version': 1, 'summary': 'Too early'})
        with self.assertRaises(ValueError):
            self.product.action('save_encounter', {'patient_id': 'p-003', 'appointment_id': appointment['id'], 'version': 1, 'summary': 'Wrong patient'})

    def test_cli_journey_executes_shared_service(self):
        result = subprocess.run([sys.executable, str(ROOT / 'cli.py'), '--data-dir', self.temp.name, 'journey'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output['appointment']['status'], 'completed')
        self.assertEqual(output['offline_replay']['results'][0]['status'], 'synced')

    def test_empty_offline_identifier_is_invalid_and_cannot_create_patient(self):
        before = len(self.product.state()['patients'])
        result = self.product.action('sync', {'operations': [{'id': '', 'role': 'reception', 'name': 'create_patient', 'payload': {'name': 'Should not exist'}}]})
        self.assertEqual(result['results'][0]['status'], 'invalid')
        self.assertEqual(len(self.product.state()['patients']), before)

    def test_duplicate_encounter_identifier_reports_conflict(self):
        p = self.patient()
        a = self.book(p['id'])
        self.product.action('set_status', {'id': a['id'], 'version': 1, 'status': 'arrived'})
        self.product.action('set_role', {'role': 'doctor'})
        self.product.action('set_status', {'id': a['id'], 'version': 2, 'status': 'in_progress'})
        payload = {'id': 'enc-duplicate-01', 'patient_id': p['id'], 'appointment_id': a['id'], 'version': 1, 'summary': 'First note'}
        self.product.action('save_encounter', payload)
        with self.assertRaises(RuntimeError):
            self.product.action('save_encounter', {**payload, 'version': 2})


if __name__ == '__main__':
    unittest.main()
