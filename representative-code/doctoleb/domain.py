"""Validation and workflow rules shared by the clinic service and CLI."""
from datetime import date
import re
import uuid

ROLES = ['reception', 'doctor', 'admin']
DOCTORS = [
    {'id': 'doctor-1', 'name': 'Dr. Noura Khalil', 'specialty': 'Family medicine', 'initials': 'NK'},
    {'id': 'doctor-2', 'name': 'Dr. Sami Mansour', 'specialty': 'Internal medicine', 'initials': 'SM'},
]
TRANSITIONS = {'scheduled': ['arrived', 'cancelled'], 'arrived': ['in_progress', 'cancelled'], 'in_progress': ['completed'], 'completed': [], 'cancelled': []}


def identifier(value, prefix=''):
    value = value or prefix + uuid.uuid4().hex
    if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{5,80}', value):
        raise ValueError('Invalid record identifier')
    return value


def text(value, label, minimum=0, maximum=200):
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        raise ValueError(f'{label} must be {minimum} to {maximum} characters')
    return value.strip()


def patient_fields(payload):
    dob = payload.get('dob', '')
    if dob:
        try:
            dob = date.fromisoformat(dob).isoformat()
        except (ValueError, TypeError):
            raise ValueError('Use a valid date of birth')
        if dob > date.today().isoformat():
            raise ValueError('Date of birth cannot be in the future')
    sex = payload.get('sex', 'unspecified')
    if sex not in ['female', 'male', 'unspecified']:
        raise ValueError('Choose a valid sex value')
    return {
        'name': text(payload.get('name', ''), 'Patient name', 2, 80),
        'dob': dob,
        'phone': text(payload.get('phone', ''), 'Phone', 0, 40),
        'sex': sex,
        'administrative_note': text(payload.get('administrative_note', ''), 'Administrative note', 0, 500),
    }


def appointment_fields(payload):
    doctor = payload.get('doctor_id', 'doctor-1')
    if doctor not in [x['id'] for x in DOCTORS]:
        raise ValueError('Choose an existing doctor')
    try:
        day = date.fromisoformat(payload.get('date', '')).isoformat()
    except (ValueError, TypeError):
        raise ValueError('Use a valid appointment date')
    time = payload.get('time', '')
    if not isinstance(time, str) or not re.fullmatch(r'([01][0-9]|2[0-3]):[0-5][0-9]', time):
        raise ValueError('Use a valid appointment time')
    duration = payload.get('duration', 30)
    if isinstance(duration, bool) or not isinstance(duration, int) or not 15 <= duration <= 120:
        raise ValueError('Duration must be 15 to 120 minutes')
    if minutes(time) + duration > 1440:
        raise ValueError('Appointment must end on the selected day')
    return {'doctor_id': doctor, 'date': day, 'time': time, 'duration': duration, 'reason': text(payload.get('reason', 'Consultation'), 'Reason', 1, 200)}


def minutes(time):
    hour, minute = time.split(':')
    return int(hour) * 60 + int(minute)


def version_matches(row, payload):
    if payload.get('version') != row['version']:
        raise RuntimeError('Record changed. Refresh and review before applying this edit')
