from flask import url_for
from .conftest import assert_msg
from app.models import User


def test_return_certmaster_orgs(client):
    client.api_user = find_user_by_name('certmaster')
    rv = client.get(url_for('cp.get_cp_organizations'))
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    got_abbreviations = [i['abbreviation'] for i in got[0]]
    expect_abbreviations = ['cert', 'evn', 'evn-gas', 'evn-strom',
                            'verbund', 'verbund-gas', 'verbund-strom',
                            'verbund-strom-leitung']
    assert set(got_abbreviations) == set(expect_abbreviations)


def test_return_verbund_admin_orgs(client):
    client.api_user = find_user_by_name('Verbund Admin')
    rv = client.get(url_for('cp.get_cp_organizations'))
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    got_abbreviations = [i['abbreviation'] for i in got[0]]
    expect_abbreviations = ['verbund', 'verbund-gas', 'verbund-strom',
                            'verbund-strom-leitung']
    assert set(got_abbreviations) == set(expect_abbreviations)


def test_return_verbund_ciso_orgs(client):
    client.api_user = find_user_by_name('Verbund CISO')
    rv = client.get(url_for('cp.get_cp_organizations'))
    assert rv.status_code == 200
    assert len(rv.json['organizations']) == 0, 'no organizations'


def test_delete_self_fails(client):
    client.api_user = find_user_by_name('Verbund CISO')
    rv = client.delete(
        url_for('cp.delete_cp_user', user_id=client.api_user.id))
    assert rv.status_code == 403


def test_delete_user_higher_up_fails(client):
    client.api_user = find_user_by_name('Verbund CISO')
    certmaster_user = find_user_by_name('certmaster')
    rv = client.delete(
        url_for('cp.delete_cp_user', user_id=certmaster_user.id))
    assert rv.status_code == 403


def test_delete_managed_user_works(client):
    client.api_user = find_user_by_name('certmaster')
    verbund_ciso_user = find_user_by_name('Verbund CISO')

    rv = client.get(url_for('cp.get_cp_organization_memberships'))
    got = list(rv.json.values())
    membership_ids_before = [i['id'] for i in got[0]]

    rv = client.delete(
        url_for('cp.delete_cp_user', user_id=verbund_ciso_user.id))
    assert rv.status_code == 200

    rv = client.get(url_for('cp.get_cp_organization_memberships'))
    got = list(rv.json.values())
    membership_ids_after = [i['id'] for i in got[0]]
    assert set(membership_ids_before) != set(membership_ids_after)


def find_user_by_name(name):
    return User.query.filter_by(name=name).first()
