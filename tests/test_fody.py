from app.fody_models import FodyOrganization
from app.models import Organization, FodyOrg_X_Organization
from app import db
import datetime
import pytest

# from .conftest import assert_msg
# from app.fixtures import testfixture


def test_fody_organization():
    fody_org = FodyOrganization(ripe_org_hdl = 'ORG-AGNS1-RIPE')
    assert fody_org.ripe_org_hdl == 'ORG-AGNS1-RIPE', 'found ripe handle'
    assert fody_org.name == 'AT&T Global Network Services Nederland B.V.', 'found name'
    assert '195.51.233.64/26' in fody_org.cidrs, 'found cidr'
    assert '195.51.215.0/25' in fody_org.cidrs, 'found cidr'
    assert fody_org.asns == [], 'no asn'
    with pytest.raises(AttributeError):
        fody_org = FodyOrganization(ripe_org_hdl = 'blablabla')

    fody_org2 = FodyOrganization(ripe_org_hdl = 'ORG-CAGF1-RIPE')
    assert fody_org2.asns == ['12635', '15554', '25255'], 'asns'
    assert fody_org2.abusecs == ['abuse@drei.com'], 'abuse contacts'


def test_link_fody_org():
    forg_x_org = FodyOrg_X_Organization();
    certorg = Organization.query.filter_by(abbreviation='cert').first()
    forg_x_org.organization_id = certorg.id
    forg_x_org.ripe_org_hdl = 'ORG-AGNS1-RIPE'
    db.session.add(forg_x_org)
    db.session.commit()

    for ripe_org in certorg.ripe_organizations:
        assert ripe_org.ripe_org_hdl == 'ORG-AGNS1-RIPE'

    certorg.upsert_ripe_handles(['ORG-AGNS1-RIPE', 'ORG-AAPA1-RIPE'])
    db.session.add(certorg)
    db.session.commit()

    current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert current_ripe_handles == ['ORG-AGNS1-RIPE', 'ORG-AAPA1-RIPE']

    certorg.upsert_ripe_handles(['ORG-AAPA1-RIPE', 'ORG-CA1-RIPE'])
    db.session.add(certorg)
    db.session.commit()

    current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert current_ripe_handles == ['ORG-AAPA1-RIPE', 'ORG-CA1-RIPE']

    certorg.upsert_ripe_handles([])
    db.session.add(certorg)
    db.session.commit()
    # current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert certorg.ripe_handles == []

