"""Exercise the independently launched package, built assets and source archive."""
import io
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        with socket.socket() as socket_:
            socket_.bind(('127.0.0.1', 0))
            port = socket_.getsockname()[1]
        cls.base = f'http://127.0.0.1:{port}'
        cls.process = subprocess.Popen([sys.executable, str(ROOT / 'serve.py'), '--port', str(port), '--data-dir', cls.temp.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(60):
            try:
                with urlopen(cls.base + '/api/health', timeout=1) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                time.sleep(.05)
        else:
            cls.process.terminate()
            cls.process.communicate(timeout=3)
            cls.temp.cleanup()
            raise RuntimeError('Independent service failed to launch')

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.communicate(timeout=5)
        cls.temp.cleanup()

    def get(self, path):
        with urlopen(self.base + path) as response:
            return response.read()

    def post(self, name, payload):
        request = Request(self.base + '/api/' + name, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        with urlopen(request) as response:
            return json.loads(response.read())

    def test_independent_server_serves_real_build_worker_fonts_and_patient_workflow(self):
        self.assertTrue((ROOT / 'dist/index.html').is_file(), 'Run npm run build before HTTP verification')
        document = self.get('/').decode()
        assets = re.findall(r'(?:src|href)="(/assets/[^\"]+)"', document)
        self.assertGreaterEqual(len(assets), 2)
        for asset in assets:
            self.assertGreater(len(self.get(asset)), 100)
        self.assertIn('CACHE_ASSETS', self.get('/sw.js').decode())
        self.assertGreater(len(self.get('/fonts/dm-sans.ttf')), 1000)
        created = self.post('create_patient', {'name': 'HTTP patient', 'phone': '+961 00 000 555'})
        state = json.loads(self.get('/api/state'))
        self.assertEqual(next(p for p in state['patients'] if p['id'] == created['id'])['phone'], '+961 00 000 555')

    def test_source_archive_contains_independent_offline_and_font_sources(self):
        with zipfile.ZipFile(io.BytesIO(self.get('/api/source.zip'))) as archive:
            files = set(archive.namelist())
            for expected in ['doctoleb/serve.py', 'doctoleb/service.py', 'doctoleb/domain.py', 'doctoleb/cli.py', 'doctoleb/package.json', 'doctoleb/public/sw.js', 'doctoleb/public/fonts/dm-sans.ttf', 'doctoleb/public/fonts/DM-Sans-OFL.txt', 'doctoleb/fixtures/clinic.json']:
                self.assertIn(expected, files)
            self.assertFalse(any('.product-data' in file or 'node_modules' in file or '/dist/' in file or file.endswith('.sqlite3') for file in files))


if __name__ == '__main__':
    unittest.main()
