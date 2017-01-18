import json
import time
from flask import url_for
from flask_login import current_user
import onetimepass
from app.models import User
from tests import DOTestCase
from unittest.mock import patch


class AuthTestCase(DOTestCase):

    def setUp(self):
        super(AuthTestCase, self).setUp()
        self.current_user = User.create_test_user()

    def create_organization(self):
        return self.client.post(
            url_for('api.add_organization'),
            data=json.dumps(dict(
                abbreviation="CERT-EU",
                full_name="Computer Emergency Response Team for EU "
                          "Institutions Agencies and Bodies",
                ip_ranges=["212.8.189.16/28"],
                abuse_emails=["cert-eu@ec.europa.eu"],
                contact_emails=[{"email": self.current_user.email}],
                asns=[5400],
                fqdns=["cert.europa.eu"]
            )),
            headers=self.get_req_headers()
        )

    def test_login_logout(self):
        rv = self.login('invalid@test.com', 'invalid')
        self.assertTrue(rv.status_code == 401)

        rv = self.login(self.current_user.email)
        rv = self.login(self.current_user.email)
        self.assertTrue(rv.status_code == 200)
        rv = self.logout()
        self.assertJSONIsNotNone(rv, 'logged_out')

    @patch.object(onetimepass, 'valid_totp')
    def test_verify_totp(self, patched_totp):
        patched_totp.return_value = True
        self.app.config['CP_WEB_ROOT'] = 'https://localhost'
        self.current_user.otp_enabled = True
        with self.client.session_transaction() as sess:
            self.login(self.current_user.email)
            rv = self.client.post(
                url_for('auth.verify_totp'),
                headers=self.get_req_headers(),
                data=json.dumps(dict(
                    totp=123456
                ))
            )
            self.assertTrue(rv.status_code == 200)

    @patch.object(onetimepass, 'valid_totp')
    def test_a_toggle_2fa(self, patched_totp):
        self.login(self.current_user.email)
        patched_totp.return_value = True
        for toggle in (True, False):
            rv = self.client.post(
                url_for('auth.toggle_2fa'),
                headers=self.get_req_headers(),
                data=json.dumps(dict(
                    totp=123456,
                    otp_toggle=toggle
                ))
            )
            self.assertTrue(rv.status_code == 200)

    def test_cp_webroot_login(self):
        self.logout()
        self.app.config['CP_WEB_ROOT'] = 'https://localhost'
        rv = self.login(self.current_user.email)
        self.assertTrue(rv.status_code == 200)
        self.logout()

    def test_auth_brute_force(self):
        codes = []
        for i in range(11):
            rv = self.client.post(
                url_for('auth.login'),
                data=json.dumps(dict(email='zxxx', password='xxxx')),
                headers=self.get_req_headers()
            )
            codes.append(rv.status_code)
        self.assertTrue(401 and 429 in codes)

    def test_bosh(self):
        # sleep 2 seconds to clear the effects of test_auth_brute_force
        time.sleep(2)
        self.login(self.current_user.email)
        rv = self.client.get(
            url_for('auth.do_bosh_auth'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        json_data = json.loads(rv.data.decode('utf-8'))
        self.assertDictEqual(
            json_data,
            {
                'service': self.app.config['BOSH_SERVICE'],
                'rooms': self.app.config['ROOMS'],
                'jid': 'test@abusehelperlab.cert.europa.eu/test-666',
                'rid': 4387476,
                'sid': '205be616f1bc48cc9ca7e405fa08adb7098af809',
            }
        )

    def test_my_account(self):
        self.login(self.current_user.email)

        rv = self.client.get(
            url_for('auth.account'),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'email', self.current_user.email)
        self.assertJSONMsg(rv, 'api_key', self.current_user.api_key)

    def test_reset_api_key(self):
        old_api_key = self.current_user.api_key
        self.login(self.current_user.email)

        rv = self.client.get(
            url_for('auth.reset_api_key'),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', 'Your API key has been reset')
        self.assertFalse(self.current_user.api_key == old_api_key)

    def test_set_password(self):
        self.login(self.current_user.email)
        token = self.current_user.generate_reset_token()
        rv = self.client.post(
            url_for('auth.set_password', token=token),
            headers={'Accept': 'application/json'},
            follow_redirects=True,
            data=dict(password='iwdw7PS8p9kO8G0WUIGrkdhE6',
                      confirm_password='iwdw7PS8p9kO8G0WUIGrkdhE6')
        )
        self.assertTrue(rv.status_code == 200)

    def test_change_password(self):
        self.login(self.current_user.email)
        self.current_user.password = old_password = 'changeme'

        rv = self.client.post(
            url_for('auth.change_password'),
            data=json.dumps(dict(
                current_password='not-old-pass',
                new_password='changedpass',
                confirm_password='changedpass'
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', 'Invalid current password', 400)

        rv = self.client.post(
            url_for('auth.change_password'),
            data=json.dumps(dict(
                current_password=old_password,
                new_password='changedpass',
                confirm_password='changedpassmiss'
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, 'message', 'Confirmation password does not match', 400)

        rv = self.client.post(
            url_for('auth.change_password'),
            data=json.dumps(dict(
                current_password=old_password,
                new_password='changedpass',
                confirm_password='changedpass'
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', 'Your password has been updated')

        with self.assertRaises(AttributeError):
            cantread = self.current_user.password

    def test_register_unregister_cp_account(self):
        self.login(self.current_user.email)
        rv = self.create_organization()
        self.assertTrue(rv.status_code == 201)
        json_data = json.loads(rv.data.decode('utf-8'))
        org = json_data['organization']

        rv = self.client.post(
            url_for('auth.register'),
            data=json.dumps(dict(
                organization_id=org['id'],
                name=org['abbreviation'] + ' (some@other7e405fa08adb709.com)',
                email='some@other7e405fa08adb709.com'
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

        rv = self.client.post(
            url_for('auth.unregister'),
            data=json.dumps(dict(
                organization_id=org['id'],
                name=org['abbreviation'] + ' (some@other7e405fa08adb709.com)',
                email='some@other7e405fa08adb709.com'
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
