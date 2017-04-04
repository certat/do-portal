from flask import url_for
from .conftest import assert_msg


def test_return_organization_user_roles(client):
    rv = client.get(url_for('cp.get_cp_organization_user_roles'))
    assert_msg(rv, key='organization_user_roles')
    print(rv)

    rv = client.get(url_for('cp.get_cp_organization_user_role', role_id=1))
    assert_msg(rv, key='display_name')
