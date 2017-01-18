from flask import url_for
from tests import DOTestCase
from app.models import User


class ExportsTestCase(DOTestCase):

    def setUp(self):
        super(ExportsTestCase, self).setUp()
        self.current_user = User.create_test_user()
        self.login(self.current_user.email)

    def test_export_ip_ranges_csv(self):
        rv = self.client.get('/export')
        self.assertTrue(rv.content_type == 'text/csv')
        self.assertEqual(
            rv.headers.get('Content-Disposition'),
            'attachment; filename=export.csv'
        )

    def test_export_ip_ranges_json(self):
        rv = self.client.get(
            url_for('main.export', export_format='json'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, key='ip_ranges')
