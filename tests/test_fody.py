from app.models import Organization, FodyOrg_X_Organization, FodyOrganization
from app.models import NotificationSetting
from app import db
import datetime
import pytest
from pprint import pprint

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

    certorg.ripe_handles = ['ORG-AGNS1-RIPE', 'ORG-AAPA1-RIPE']
    db.session.add(certorg)
    db.session.commit()

    current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert current_ripe_handles == ['ORG-AGNS1-RIPE', 'ORG-AAPA1-RIPE']

    certorg.ripe_handles = ['ORG-AAPA1-RIPE', 'ORG-CA1-RIPE']
    db.session.add(certorg)
    db.session.commit()

    current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert current_ripe_handles == ['ORG-AAPA1-RIPE', 'ORG-CA1-RIPE']

    certorg.ripe_handles = []
    db.session.add(certorg)
    db.session.commit()
    # current_ripe_handles = [ro.ripe_org_hdl for ro in certorg.ripe_organizations]
    assert certorg.ripe_handles == []

def test_settings():
    forg_x_org = FodyOrg_X_Organization();
    certorg = Organization.query.filter_by(abbreviation='cert').first()
    forg_x_org.organization_id = certorg.id
    forg_x_org.ripe_org_hdl = 'ORG-CAGF1-RIPE'
    db.session.add(forg_x_org)
    db.session.commit()
    # fody_org = FodyOrg_X_Organization(ripe_org_hdl = 'ORG-CAGF1-RIPE')
    # assert forg_x_org.asns == ['12635', '15554', '25255'], 'asns'
    #assert forg_x_org.abusecs == ['abuse@drei.com'], 'abuse contacts'

    with pytest.raises(AttributeError):
        forg_x_org.upsert_notification_setting(asn = '12635123123',
                                     notification_interval = 4711)

    forg_x_org.upsert_notification_setting(asn = '12635',
                                         notification_interval = 4711)

    db.session.commit()
    forg_x_org.upsert_notification_setting(asn = '12635',
                                         notification_interval = 4713)
    db.session.commit()
    forg_x_org.upsert_notification_setting(cidr = '94.245.192.0/18',
                                         notification_interval = 47)
    db.session.commit()
    nss = NotificationSetting.query. \
           filter(NotificationSetting.ripe_org_hdl=='ORG-CAGF1-RIPE')
    for ns  in nss:
        print(ns.asn ,ns.cidr)
    pprint(forg_x_org.notification_settings)

    assert forg_x_org.notification_settings['asns'][0]['12635']['notification_interval'] == 4713
#    assert forg_x_org.notification_settings['cidrs'][0]['notification_interval'] == 47

