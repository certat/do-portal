from flask import url_for
from .conftest import assert_msg
from app.models import User


def test_return_certmaster_orgs(client):
    client.api_user = User.query.filter_by(name='certmaster').first()
    rv = client.get(url_for('cp.get_cp_organizations'))
    print(rv.json)
    assert_msg(rv, key='abbreviation')
