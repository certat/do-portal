from flask import url_for
from .conftest import assert_msg
from pprint import pprint
from app.models import User, Organization
from requests.utils import quote

def test_get_handle_data(client):
    rv = client.get(url_for('cp.get_cp_ripe_handle',
                        ripe_org_hdl='ORG-AA83-RIPE'))

    assert rv.json['asns'][0] == '29429'
    assert rv.json['cidrs'] == ['195.245.92.0/23']


def test_create_setting(client):

    rv = client.post(
        url_for('cp.add_cp_organization'),
        json=dict(abbreviation="setting-org",
                  full_name="setting-org",
                  parent_org_id=client.test_user.organization_id,
                  ripe_handles=['ORG-AA83-RIPE'])
    )

    org = Organization.query.filter_by(abbreviation='setting-org').one()
    rv = client.post(
               url_for('cp.set_cp_settings',
                     ripe_org_hdl='ORG-AA83-RIPE',
                     org_id=org.id),
                json = {'cidr': '195.245.92.0/23',
                          'notification_setting': {
                             'notification_interval': '0815'
                          }
                       }
                )
    assert rv.status_code == 201

    rv = client.get(url_for('cp.get_cp_settings',
                        ripe_org_hdl='ORG-AA83-RIPE',
                        org_id=org.id
                    ))

    assert rv.json['cidrs'][0]['notification_setting']['notification_interval'] ==  815

    cidr = quote('195.245.92.0/23', safe='')
    rv = client.get(url_for('cp.get_cp_contact_for_netblock',
                            cidr=cidr))

    assert rv.json['notification_setting']['organization_id'] == org.id
    assert rv.json['abusecs'] == ['abuse@nextlayer.at']

    cidr = quote('195.245.92.0/24', safe='')
    rv = client.get(url_for('cp.get_cp_contact_for_netblock',
                            cidr=cidr))

    assert rv.json['notification_setting']['organization_id'] == org.id
    assert rv.json['abusecs'] == ['abuse@nextlayer.at']

    cidr = quote('1.2.2.3aa', safe='')
    rv = client.get(url_for('cp.get_cp_contact_for_netblock',
                            cidr=cidr))
    assert rv.status_code == 421

    cidr = quote('1.2.2.3', safe='')
    rv = client.get(url_for('cp.get_cp_contact_for_netblock',
                            cidr=cidr))
    assert rv.status_code == 404
