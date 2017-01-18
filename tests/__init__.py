import unittest
import json
from collections import namedtuple
from io import BytesIO
import hashlib
import ssdeep
from flask import url_for
from app import create_app, db
from flask_ldap3_login import AuthenticationResponse
from flask_ldap3_login import AuthenticationResponseStatus
from app.utils import bosh_client
import flask_gnupg
# upgrade test to py.test
# mock is included in python 3.3
# tests can be updated to use it without 3rd party deps
# import mock


Sample = namedtuple(
    'Sample', ['data', 'filename', 'md5', 'sha1', 'sha256', 'sha512', 'ctph'])


def create_sample(data, filename=None):
    if filename is None:
        filename = 'blah.zip'
    sampledata = BytesIO(data)
    buf = sampledata.read()
    sampledata.seek(0)
    md5_hash = hashlib.md5(buf).hexdigest()
    sha1_hash = hashlib.sha1(buf).hexdigest()
    sha256_hash = hashlib.sha256(buf).hexdigest()
    sha512_hash = hashlib.sha512(buf).hexdigest()
    ctph = ssdeep.hash(buf)

    sample = Sample(
        data=sampledata, filename=filename, md5=md5_hash, sha1=sha1_hash,
        sha256=sha256_hash, sha512=sha512_hash, ctph=ctph)
    return sample


def fake_auth(username, password):
    """Fake auth

    :param username:
    :param password:
    :return:
    """
    if username == 'test':
        return AuthenticationResponse(AuthenticationResponseStatus.success)
    else:
        return AuthenticationResponse(AuthenticationResponseStatus.fail)


def fake_user_info(username):
    """Fake LDAP user info

    :param username:
    :return:
    """

    return {
        'accountExpires': ['9223372036854775807'],
        'badPasswordTime': ['130991409187680061'],
        'badPwdCount': ['0'],
        'cn': ['Test Account'],
        'company': ['CERT-EU'],
        'countryCode': ['0'],
        'description': ['CERT-EU Staff'],
        'displayName': ['Test Account'],
        'dn': 'CN=Test Account,OU=Users,OU=CERT-EU,DC=cert,DC=europa,DC=eu',
        'givenName': ['Test'],
        'mail': ['test@cert.europa.eu'],
        'name': ['Test Account'],
        'mailNickname': ['test'],
        'userPrincipalName': ['test@cert.europa.eu']
    }


class FakeBOSHClient(object):

    def __init__(self, username, password, service):
        self.jid = 'test@abusehelperlab.cert.europa.eu/test-666'
        self.rid = 4387476
        self.sid = '205be616f1bc48cc9ca7e405fa08adb7098af809'

    def start_session_and_auth(self, hold=1, wait=2):
        return True


class DOTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        # self.old_auth = auth.routes.do_ldap_authentication
        # auth.routes.do_ldap_authentication = fake_do_ldap_authentication
        self.old_ldap_auth = self.app.ldap3_login_manager.authenticate_search_bind
        self.app.ldap3_login_manager.authenticate_search_bind = fake_auth

        self.old_user_info = self.app.ldap3_login_manager.get_user_info_for_username
        self.app.ldap3_login_manager.get_user_info_for_username = fake_user_info

        self.old_bosh_client = bosh_client.BOSHClient
        bosh_client.BOSHClient = FakeBOSHClient

    def tearDown(self):
        # auth.routes.do_ldap_authentication = self.old_auth
        self.app.ldap3_login_manager.authenticate_search_bind = self.old_ldap_auth
        self.app.ldap3_login_manager.get_user_info_for_username = self.old_user_info
        bosh_client.BOSHClient = self.old_bosh_client
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_req_headers(self, token=None):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if token is not None:
            headers['Cookie'] = "rm=" + token
        return headers

    def login(self, email='test@test.com', password='e9c9525ef737'):
        return self.client.post(
            url_for('auth.login'),
            data=json.dumps(dict(email=email, password=password)),
            headers=self.get_req_headers()
        )

    def logout(self):
        return self.client.get(
            url_for('auth.logout'),
            headers=self.get_req_headers()
        )

    def assertWordinResponse(self, response, value, response_code=None):
        if response_code is None:
            response_code = 200
        self.assertTrue(response.status_code == response_code)
        self.assertTrue(bytes(value, encoding='utf8') in response.data)

    def assertJSONIsNotNone(self, response, key, response_code=None):
        if response_code is None:
            response_code = 200
        self.assertTrue(response.status_code == response_code)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data[key])

    def assertJSONMsg(self, rv, key=None, value=None, rv_status=None):
        """

        :param rv: Response value
        :param key: Key in the JSON response to check
        :param value: Value to check
        :param rv_status:
        :return:
        """
        if key is None:
            key = 'message'
        if rv_status is None:
            rv_status = 200
        self.assertTrue(rv.status_code == rv_status)
        json_rv = json.loads(rv.data.decode('utf-8'))
        self.assertTrue(json_rv[key] == value)
        # test exceptions
        # with self.assertRaises(TypeError):
        #     obj.method()

    def __repr__(self):
        return '<%r>' % self.__class__.__name__
