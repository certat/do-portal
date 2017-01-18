import json
from flask import url_for
from app.models import User
from tests import DOTestCase


class VulnerabilitiesTestCase(DOTestCase):

    current_user = None

    def setUp(self):
        super().setUp()
        self.current_user = User.create_test_user()
        self.login(self.current_user.email)

    def tearDown(self):
        self.current_user = None
        super().tearDown()

    def create_organization(self):
        return self.client.post(
            url_for('api.add_organization'),
            data=json.dumps(dict(
                abbreviation="DUMMY",
                full_name="Damn ugly might mean yummy",
                ip_ranges=["66.66.66.66/16"],
                abuse_emails=["admin@dummy.yummy"],
                contact_emails=[{"email": "admin@dummy.yummy"}],
                asns=[666],
                fqdns=["dummy.yummy"]
            )),
            headers=self.get_req_headers()
        )

    def create_vuln(self, org_id):
        return self.client.post(
            url_for('api.add_vulnerability'),
            data=json.dumps(dict(
                organization_id=org_id,
                url='http://hear-me-roar.tld/forest',
                check_string='--></script><script>alert("Honey")</script>',
                reporter_name='Yoggy',
                reporter_email='yoggy@hear-me-roar.frst',
                rtir_id=666,
                types=['XSS', 'berries']
            )),
            headers=self.get_req_headers()
        )

    def test_vulnerabilities(self):
        rv = self.create_organization()
        self.assertJSONMsg(rv, value='Organization added', rv_status=201)
        json_rv = json.loads(rv.data.decode('utf-8'))
        org = json_rv['organization']

        rv = self.create_vuln(org['id'])
        self.assertJSONIsNotNone(rv, 'vulnerability', 201)

        rv = self.client.put(
            url_for('api.update_vulnerability', vuln_id=1),
            data=json.dumps(dict(
                organization_id=org['id'],
                url='http://hear-me-roar.tld/forest',
                check_string='--></script><script>alert("Moar moar")</script>',
                reporter_name='Yoggy',
                reporter_email='yoggy@hear-me-roar.frst',
                rtir_id=666,
                types=['XSS', 'cherries']
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Vulnerability saved')

        rv = self.client.get(
            url_for('api.get_vulnerabilities'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        rv = self.client.get(
            url_for('api.get_vulnerability', vuln_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        rv = self.client.delete(
            url_for('api.delete_vulnerability', vuln_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Vulnerability deleted')

    def test_cp_vulnerabilities(self):

        rv = self.create_organization()
        self.assertJSONMsg(rv, value='Organization added', rv_status=201)
        json_rv = json.loads(rv.data.decode('utf-8'))
        org = json_rv['organization']

        rv = self.create_vuln(org['id'])
        self.assertJSONIsNotNone(rv, 'vulnerability', 201)

        rv = self.client.get(
            url_for('cp.get_vulnerabilities'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
