from flask import url_for
from .conftest import assert_msg


def test_create_org(client):
    rv = client.post(
        url_for('cp.add_cp_organization'),
        json=dict(abbreviation="CERT-EU",
                  full_name="Computer Emergency Response Team for EU "
                            "Institutions Agencies and Bodies",
                  ip_ranges=["212.8.189.16/28"],
                  abuse_emails=["cert-eu@ec.europa.eu"],
                  contact_emails=[{"email": "cert-eu@ec.europa.eu"}],
                  asns=[5400],
                  fqdns=["cert.europa.eu"],
                  parent_org_id=client.test_user.organization_id)
    )
    assert_msg(rv, value='Organization added', response_code=201)


def test_update_org(client):
    rv = client.put(
        url_for('cp.update_cp_organization',
                org_id=client.test_user.organization_id),
        json=dict(abbreviation="CERT-EU",
                  full_name="Computer Emergency Response Team for EU "
                            "Institutions Agencies and Bodies",
                  ip_ranges=["212.8.189.16/28"],
                  abuse_emails=["cert-eu@ec.europa.eu"],
                  contact_emails=[{"email": "cert-eu-new@ec.europa.eu"}],
                  asns=[5400],
                  fqdns=["cert.europa.eu"],
                  parent_org_id=client.test_user.organization_id)
    )
    assert rv.status_code == 200


def test_return_orgs(client):
    rv = client.get(url_for('cp.get_cp_organizations'))
    assert_msg(rv, key='organizations')

    rv = client.get(url_for('cp.get_cp_organization',
                    org_id=client.test_user.organization_id))
    assert_msg(rv, key='abbreviation')


def test_del_org(client):
    rv = client.delete(url_for('cp.delete_cp_organization',
                       org_id=client.test_user.organization_id))
    assert_msg(rv, value='Organization deleted')

    rv = client.delete(url_for('cp.delete_cp_organization', org_id=666))
    assert rv.status_code == 404
