import json
import os
import shutil
from flask import url_for
from tests import DOTestCase
import gnupg
from app.models import User


class FakeGPG(gnupg.GPG):

    def search_keys(self, query, keyserver='pgp.mit.edu'):
        return [{
            'algo': '1',
            'date': '1353431464',
            'expires': '',
            'keyid': '480183F5942E91953F377D6C64CDC60B16E645C6',
            'length': '2048',
            'type': 'pub',
            'uids': ['Vicente <vicente.revuelto@gmail.com>',
                     'Vicente Prueba <vicente.prueba@test.com>',
                     'Vicente Revuelto <vrevuelto@cert.europa.eu>']
        }]

    def recv_keys(self, keyserver, *keyids):
        ir = gnupg.ImportResult(self)
        ir.fingerprints = ['480183F5942E91953F377D6C64CDC60B16E645C6']
        ir.imported = 1
        ir.imported_rsa = 1
        return ir

    def send_keys(self, keyserver, *keyids):
        return

    def import_keys(self, key_data):
        ir = gnupg.ImportResult(self)
        ir.fingerprints = ['480183F5942E91953F377D6C64CDC60B16E645C6']
        ir.imported = 1
        ir.imported_rsa = 1
        return ir

    def encrypt(self, data, recipients, **kwargs):
        er = gnupg.Crypt(self)
        er.ok = True
        return er


class GPGTestCase(DOTestCase):

    @classmethod
    def setUpClass(cls):
        gnupg.GPG = FakeGPG

    def setUp(self):
        super(GPGTestCase, self).setUp()
        self.current_user = User.create_test_user()

    def tearDown(self):
        gpg_path = self.app.config['GPG_HOME']
        if os.path.isdir(gpg_path):
            shutil.rmtree(gpg_path)
        super(GPGTestCase, self).tearDown()

    def test_key_search(self):
        rv = self.client.post(
            url_for('api.search_public_ks'),
            data=json.dumps(dict(email='test@cert.europa.eu')),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 401)

        self.login(self.current_user.email)
        rv = self.client.post(
            url_for('api.search_public_ks'),
            data=json.dumps(dict(email='test@cert.europa.eu')),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, key='keys')

    def test_import_keys(self):
        self.login(self.current_user.email)
        rv = self.client.post(
            url_for('api.import_keys'),
            data=json.dumps(
                dict(keys=['480183F5942E91953F377D6C64CDC60B16E645C6'])
            ),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Imported', rv_status=201)

    def test_send_keys(self):
        self.login(self.current_user.email)
        key_file_path = os.path.join(os.path.dirname(__file__), '16E645C6.asc')
        kfp = open(key_file_path)
        rv = self.client.post(
            url_for('api.submit_gpg_key'),
            data=json.dumps(dict(ascii_key=kfp.read())),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Key saved', rv_status=201)
