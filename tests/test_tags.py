import json
from flask import url_for
from app.models import User
from tests import DOTestCase


class TagsTestCase(DOTestCase):

    current_user = None

    def setUp(self):
        super().setUp()
        self.current_user = User.create_test_user()
        self.login(self.current_user.email)

    def tearDown(self):
        self.current_user = None
        super().tearDown()

    def test_tags(self):
        rv = self.client.post(
            url_for('api.add_tag'),
            data=json.dumps(dict(
                name='Boobo',
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'tag', 201)

        rv = self.client.put(
            url_for('api.update_tag', tag_id=1),
            data=json.dumps(dict(
                name='Yoggy',
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Tag saved')

        rv = self.client.get(
            url_for('api.get_tags'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        rv = self.client.get(
            url_for('api.get_tag', tag_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        rv = self.client.delete(
            url_for('api.delete_tag', tag_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Tag deleted')
