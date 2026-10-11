"""Clinic CLI using the same persisted domain service as the browser."""
import argparse
from datetime import timedelta, date
import json
from pathlib import Path
import uuid
from service import Product


def journey(product):
    key = uuid.uuid4().hex[:10]
    today = product.state()['today']
    visit_day = (date.fromisoformat(today) + timedelta(days=1)).isoformat()
    product.action('set_role', {'role': 'reception'})
    patient = product.action('create_patient', {'id': 'p-cli-' + key, 'name': 'Rana Haddad', 'dob': '1990-05-12', 'phone': '+961 00 000 123', 'sex': 'female'})
    # Use a distinct day on repeated CLI journeys to preserve scheduling rules.
    occupied = {a['date'] for a in product.state()['appointments'] if a['time'] == '16:00' and a['doctor_id'] == 'doctor-1'}
    while visit_day in occupied:
        visit_day = (date.fromisoformat(visit_day) + timedelta(days=1)).isoformat()
    appointment = product.action('create_appointment', {'patient_id': patient['id'], 'doctor_id': 'doctor-1', 'date': visit_day, 'time': '16:00', 'duration': 30, 'reason': 'Follow-up consultation'})
    operations = [{'id': 'op-cli-' + key, 'role': 'reception', 'name': 'set_status', 'payload': {'id': appointment['id'], 'version': 1, 'status': 'arrived'}}]
    replay = product.action('sync', {'operations': operations})
    product.action('set_role', {'role': 'doctor'})
    product.action('set_status', {'id': appointment['id'], 'version': 2, 'status': 'in_progress'})
    product.action('save_encounter', {'patient_id': patient['id'], 'appointment_id': appointment['id'], 'version': 1, 'summary': 'Follow-up completed', 'assessment': 'Progress reviewed', 'plan': 'Return in four weeks'})
    product.action('set_status', {'id': appointment['id'], 'version': 3, 'status': 'completed'})
    state = product.state()
    return {'patient': next(x for x in state['patients'] if x['id'] == patient['id']), 'appointment': next(x for x in state['appointments'] if x['id'] == appointment['id']), 'offline_replay': replay}


def main():
    parser = argparse.ArgumentParser(description='Doctoleb local clinic')
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent / '.product-data')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('state')
    commands.add_parser('journey')
    action = commands.add_parser('action')
    action.add_argument('name')
    action.add_argument('payload', help='JSON object or @path-to-json')
    args = parser.parse_args()
    product = Product(args.data_dir)
    if args.command == 'state':
        result = product.state()
    elif args.command == 'journey':
        result = journey(product)
    else:
        raw = Path(args.payload[1:]).read_text(encoding='utf-8') if args.payload.startswith('@') else args.payload
        result = product.action(args.name, json.loads(raw))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
