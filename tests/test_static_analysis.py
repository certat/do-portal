import json
from flask import url_for
from app.models import User
from tests import DOTestCase


class StaticAnalysisTestCase(DOTestCase):

    current_user = None

    def setUp(self):
        super().setUp()
        self.current_user = User.create_test_user()
        self.login(self.current_user.email)

    def tearDown(self):
        self.current_user = None
        super().tearDown()

    def test_start_static_analysis(self):
        rv = self.client.post(
            url_for('api.add_analysis'),
            data=json.dumps(dict(files=[{'sha256': '1eedab2b09a4bf6c'}])),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, key='message', rv_status=202,
            value='Your files have been submitted for static analysis')

    def test_get_static_analysis(self):
        rv = self.client.get(
            url_for('api.get_analysis', sha256='1eedab2b09a4bf6c87b273305c09'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 404)

    def test_get_static_analyses(self):
        rv = self.client.get(
            url_for('api.get_analyses'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'items')
