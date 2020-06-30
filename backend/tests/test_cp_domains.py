from flask import url_for
from app.models import User, Organization, Domain, MembershipRole, OrganizationMembership
from .conftest import assert_msg
from app import db
import pytest
import datetime

#################################################################
# Test DS
class TDS:
    toporg = 'cert'
    org1 = 'testdomain_org1'
    org2 = 'testdomain_org2'
    orgwrong = 'testdomain_org_wrongdomain'
    orgnotadmin = 'testdomain_org_notadmin'
    domain1 = 'domain1.at'
    domain2 = 'domain2.at'
    domain3 = 'domain3.at'
    domain4 = 'domain4.at'
    domainupdate = 'domainupdated.at'
    domainwrong = ' '
    domainother = 'domainother.at'
    testuser_nomember = {   "email": 'nomember@testuser.at',
                            "name": 'nomember testuser',
                            "password": 'Bla12345%',
                            "birthdate": datetime.datetime.utcnow(),
                            "title": 'TestTitle.',
                            "origin": 'testdata'
                        }
    testuser_notadmin = {   "email": 'notadmin@testuser.at',
                            "name": 'not admin testuser',
                            "password": 'Bla12345%',
                            "birthdate": datetime.datetime.utcnow(),
                            "title": 'TestTitle.',
                            "origin": 'testdata'
                        }
    testuser_otheradm = {   "email": 'otheradmin@testuser.at',
                            "name": 'other admin testuser',
                            "password": 'Bla12345%',
                            "birthdate": datetime.datetime.utcnow(),
                            "title": 'TestTitle.',
                            "origin": 'testdata'
                        }

    @staticmethod
    def adminrole():
        name = 'OrgAdmin'
        role = MembershipRole.query.filter_by(name=name).first()
        assert role, 'test broken. admin role not found'
        return role

    @staticmethod
    def notadminrole():
        name = 'CISO'
        role = MembershipRole.query.filter_by(name=name).first()
        assert role, 'test broken. role for notadmin not found'
        return role

    @staticmethod
    def topadminuser():
        email='cert@master.at'
        user = User.query.filter_by(_email=email).one()
        assert user, 'test broken. admin user not found'
        return user

    @staticmethod
    def getUser(testuserdict):
        message = ""
        user = User.query.filter_by(_name=testuserdict['name']).first()
        if not user:
            try:
                (user, message) = User.create(testuserdict)
            except Exception as e:
                assert False, 'test broken. Exception while user create. ' + str(e)

            if not user or message != "User added":
                assert False, 'test broken. user not created: ' + message
            try:
                db.session.commit()
            except Exception as e:
                assert False, 'test broken. Exception while user create commit. ' + str(e)
        return user

    @staticmethod
    def testuser_no_member():
        user = TDS.getUser(TDS.testuser_nomember)
        return user

    @staticmethod
    def testuser_not_admin():
        org = TDS.getOrganization(TDS.orgnotadmin)
        user = TDS.getUser(TDS.testuser_otheradm)
        role = TDS.notadminrole()
        oxu = OrganizationMembership.query.filter_by(organization=org, user=user, membership_role=role).first()
        if not oxu:
            oxu = OrganizationMembership(
                                        organization=org,
                                        user=user,
                                        membership_role=role)
            db.session.add(oxu)
            db.session.commit()
        assert oxu, 'test broken. membership not found.'
        return user

    @staticmethod
    def testuser_other_admin():
        org = TDS.getOrganization(TDS.org2)
        user = TDS.getUser(TDS.testuser_otheradm)
        role = TDS.adminrole()
        oxu = OrganizationMembership.query.filter_by(organization=org, user=user, membership_role=role).first()
        if not oxu:
            oxu = OrganizationMembership(
                                        organization=org,
                                        user=user,
                                        membership_role=role)
            db.session.add(oxu)
            db.session.commit()
        assert oxu, 'test broken. membership not found.'
        return user

    @staticmethod
    def find_user_by_name(name):
        return User.query.filter_by(_name=name).first()

    @staticmethod
    def getOrganization(orgname):
        parent = Organization.query.filter_by(abbreviation=TDS.toporg).first()
        org = Organization.query.filter_by(abbreviation=orgname).first()
        if not org:
            org = Organization(full_name=orgname, display_name=orgname, abbreviation=orgname, parent_org_id=parent.id)
            db.session.add(org)
            db.session.commit()
        assert org, 'test broken. organization {0} not found'.format(orgname)
        return org

    @staticmethod
    def getTopOrganization():
        org = Organization.query.filter_by(abbreviation=TDS.toporg, parent_org_id=None).first()
        assert org, 'test broken. top organization {0} not found'.format(TDS.toporg)
        return org

    def getDomain(orgname, domain_name):
        org = Organization.query.filter_by(abbreviation=orgname).first()
        assert org, 'test broken. organization {0} not found'.format(orgname)
        domain = Domain.query.filter_by(_domain_name=domain_name, organization_id=org.id).first()
        assert domain, 'test broken. domain {0} for organization {1} not found'.format(domain_name, orgname)
        return domain

###########################################################


def test_create_toporg_domain(client):
    org = TDS.getTopOrganization()
    count_domains = Domain.query.filter_by(organization_id=org.id).count()
    expectedcount = count_domains + 1

    client.api_user = TDS.topadminuser()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain1,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Domain added', response_code=201)

    assert expectedcount == Domain.query.filter_by(organization_id=org.id).count(), 'after insert domain: wrong count of domains by sql query'
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains by Organization.domains'
    

def test_create_neworg_domain(client):
    org = TDS.getOrganization(TDS.org1)
    count_domains = org.domains.count()
    expectedcount = count_domains + 1

    client.api_user = TDS.topadminuser()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain2,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Domain added', response_code=201)

    assert expectedcount == Domain.query.filter_by(organization_id=org.id).count(), 'after insert domain: wrong count of domains by sql query'
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains by Organization.domains'


def test_create_neworg_existing_domain(client):
    org = TDS.getOrganization(TDS.org1)
    count_domains = org.domains.count()
    expectedcount = count_domains

    client.api_user = TDS.topadminuser()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain2,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='already exists', response_code=422)
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains'


def test_create_same_domain_other_organization(client):
    org = TDS.getOrganization(TDS.org1)
    count_domains = org.domains.count()
    expectedcount = count_domains + 1

    client.api_user = TDS.topadminuser()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain1,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Domain added', response_code=201)
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains'


#test: create domain without any authorization for organization
def test_create_domain_not_authorized(client):
    org = TDS.getOrganization(TDS.org1)
    count_domains = org.domains.count()
    expectedcount = count_domains

    client.api_user = TDS.testuser_no_member()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain3,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Unauthorized', response_code=401)
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains'


#test: create domain with authorization other then admin
def test_create_domain_wrong_role(client):
    user = TDS.testuser_not_admin()
    org = TDS.getOrganization(TDS.orgnotadmin)
    count_domains = Domain.query.count()
    expectedcount = count_domains

    client.api_user = TDS.testuser_not_admin()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain4,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Unauthorized', response_code=401)
    assert expectedcount == Domain.query.count(), 'after insert domain: wrong count of domains'


def test_get_domains_by_organization(client):
    org = TDS.getOrganization(TDS.org1)

    client.api_user = TDS.topadminuser()

    rv = client.get(
        url_for('cp.get_cp_organization_domains', organization_id=org.id),
    )
    assert rv.status_code == 200
    #assert_msg(rv, value='OK', response_code=200)a
    expected = [TDS.domain1, TDS.domain2]
    expected.sort()
    got = list(rv.json.values())
    domains = [i['domain_name'] for i in got[0]]
    domains.sort()
    assert set(domains) == set(expected), 'Result set not as expected' 


def test_get_domains_other_organization(client):
    org = TDS.getOrganization(TDS.org2)
    count_domains = org.domains.count()
    expectedcount = count_domains + 1

    client.api_user = TDS.testuser_other_admin()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domainother,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Domain added', response_code=201)
    assert expectedcount == org.domains.count(), 'test broken. wrong count of domains'

    org = TDS.getOrganization(TDS.org1)
    rv = client.get(
        url_for('cp.get_cp_organization_domains', organization_id=org.id),
    )
    assert_msg(rv, value='Unauthorized', response_code=401)


def test_update_domain_wrong_name(client):
    newname=TDS.domainwrong
    domain = TDS.getDomain(TDS.org1, TDS.domain2)
    client.api_user = TDS.topadminuser()
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domain.id),
        json=dict(domain_name=newname)
    )
    assert_msg(rv, value='could not update', response_code=421)
    assert Domain.query.filter_by(domain_name=newname).count() == 0, 'Domain with wrong name exists after update.'


def test_create_test_ds_for_update_domain_existing(client):
    org = TDS.getTopOrganization()

    client.api_user = TDS.topadminuser()

    rv = client.post(
        url_for('cp.add_cp_domain'),
        json=dict(
            domain_name = TDS.domain3,
            organization_id = org.id
        )
    )
    assert_msg(rv, value='Domain added', response_code=201)


def test_update_domain_existing(client):
    newname=TDS.domain1
    domain = TDS.getDomain(TDS.org1, TDS.domain2)
    client.api_user = TDS.topadminuser()
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domain.id),
        json=dict(domain_name=newname)
    )
    assert_msg(rv, value='already exists', response_code=422)
    assert TDS.getDomain(TDS.org1, TDS.domain2), 'Domain name changed to existing name.'
    newname=TDS.domain3
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domain.id),
        json=dict(domain_name=newname)
    )
    assert rv.status_code == 200


def test_update_domain_unauthorized(client):
    domain = TDS.getDomain(TDS.org1, TDS.domain3)
    client.api_user = TDS.testuser_not_admin()
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domain.id),
        json=dict(domain_name=TDS.domainupdate)
    )
    assert rv.status_code == 401, 'domain updated by unauthorized user'


def test_update_domain(client):
    domain = TDS.getDomain(TDS.org1, TDS.domain3)
    client.api_user = TDS.topadminuser()
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domain.id),
        json=dict(domain_name=TDS.domainupdate)
    )
    assert rv.status_code == 200, 'domain could not be updated'


def test_get_domain(client):
    domain = TDS.getDomain(TDS.org1, TDS.domainupdate)
    client.api_user = TDS.topadminuser()

    rv = client.get(
        url_for('cp.get_cp_domain', domain_id=domain.id),
    )
    assert rv.status_code == 200


def test_get_domain_not_authorized(client):
    domain = TDS.getDomain(TDS.org1, TDS.domainupdate)
    client.api_user = TDS.testuser_not_admin()

    rv = client.get(
        url_for('cp.get_cp_domain', domain_id=domain.id),
    )
    assert_msg(rv, value='Unauthorized', response_code=401)


def test_delete_domain_not_authorized(client):
    orgname = TDS.org1
    domain = TDS.getDomain(orgname, TDS.domainupdate)
    org = TDS.getOrganization(orgname)
    count_domains = org.domains.count()
    expectedcount = count_domains

    client.api_user = TDS.testuser_not_admin()

    rv = client.delete(
        url_for('cp.delete_cp_domain', domain_id=domain.id)
    )
    assert_msg(rv, value='Unauthorized', response_code=401)
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains'


def test_delete_domain(client):
    orgname = TDS.org1
    domain = TDS.getDomain(orgname, TDS.domainupdate)
    domainid = domain.id
    org = TDS.getOrganization(orgname)
    count_domains = Domain.query.filter_by(organization_id=org.id).count()
    expectedcount = count_domains - 1

    client.api_user = TDS.topadminuser()

    rv = client.delete(
        url_for('cp.delete_cp_domain', domain_id=domain.id)
    )
    assert_msg(rv, value='Domain deleted', response_code=200)
    assert expectedcount == org.domains.count(), 'after insert domain: wrong count of domains'

    #test get on deleted domain
    rv = client.get(
        url_for('cp.get_cp_domain', domain_id=domainid),
    )
    assert_msg(rv, value='Resource not found', response_code=404)

    #test update on deleted domain
    rv = client.put(
        url_for('cp.update_cp_domain',
                domain_id=domainid),
        json=dict(domain_name=TDS.domainupdate)
    )
    assert_msg(rv, value='Resource not found', response_code=404)


def test_delete_organization_and_getdomains(client):
    orgname = TDS.org1
    org = TDS.getOrganization(orgname)
    count_domains = org.domains.count()
    count_all_domains = Domain.query.count()
    expectedcount = count_all_domains - count_domains

    client.api_user = TDS.topadminuser()

    rv = client.delete(
        url_for('cp.delete_cp_organization', org_id=org.id)
    )
    assert_msg(rv, value='Organization deleted', response_code=200)
    assert Organization.query.filter_by(abbreviation=orgname).count() == 0, 'Organization has not been deleted properly.'
    assert 0 == org.domains.count(), 'after delete organization: existing domains for organization'
    assert expectedcount == Domain.query.count(), 'after delete organization: wrong count for domains'

    #try to query domains on deleted organization
    rv = client.get(
        url_for('cp.get_cp_organization_domains', organization_id=org.id),
    )
    assert_msg(rv, value='Resource not found', response_code=404)


    

