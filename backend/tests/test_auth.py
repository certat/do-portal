import time
import pytest
from flask import url_for
from .conftest import assert_msg

from app.models import User


def test_login_logout(client):
    rv = client.post(
        url_for('auth.login'),
        json=dict(email=client.test_user.email,
                  password='1e9c9525ef737'))
    assert rv.status_code == 200


def test_reset_api_key(client):
    rv = client.get(url_for('auth.reset_api_key'))
    assert_msg(rv, value='Your API key has been reset')


def test_set_password(client):
    token = client.test_user.generate_reset_token()
    rv = client.post(
        url_for('auth.set_password', token=token),
        follow_redirects=True,
        json=dict(password='e9c9525ef737',
                  confirm_password='e9c9525ef737'))
    assert rv.status_code == 200


changepw_params = [
    ({'current_password': 'not-old-pass',
      'new_password': 'changedpass',
      'confirm_password': 'changedpass'}, 'Invalid current password', 400),
    ({'current_password': 'e9c9525ef737',
      'new_password': 'changedpass',
      'confirm_password': 'changedpassmiss'},
     'Confirmation password does not match', 400),
    ({'current_password': 'e9c9525ef737',
      'new_password': 'changedpass',
      'confirm_password': 'changedpass'},
     'Your password has been updated', 200),
]


@pytest.mark.parametrize('post_data, msg, status_code', changepw_params)
def test_change_password(client, post_data, msg, status_code):
    rv = client.post(
        url_for('auth.change_password'),
        json=post_data
    )
    assert_msg(rv, key='message', value=msg, response_code=status_code)
