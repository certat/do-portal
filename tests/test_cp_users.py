from flask import url_for
from .conftest import assert_msg
from app.models import User


def test_return_certmaster_orgs(client):
    client.api_user = User.query.filter_by(name='certmaster').first()
    rv = client.get(url_for('cp.get_cp_organizations'))
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    got_abbreviations = [i['abbreviation'] for i in got[0]]
    expect_abbreviations = ['cert', 'evn', 'evn-gas', 'evn-strom',
                            'verbund', 'verbund-gas', 'verbund-strom',
                            'verbund-strom-leitung']
    assert set(got_abbreviations) == set(expect_abbreviations)
