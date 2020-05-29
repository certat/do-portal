from .conftest import assert_msg
from app.models import User, Organization, OrganizationMembership, MembershipRole
from app import db
import pytest
import datetime

class TAU:
    org1_abbr = 'testorg1'
    org2_abbr = 'testorg2'
    org31_abbr = 'testorg3.1'
    rootuser_name = 'rootuser'
    rootuser_updatedname = 'rootuser updated'
    rootuser_email = 'root@test.alias.user'
    rootuser_password = 'Test1_aliasuser'
    rootuser_membershiprole = 'OrgAdmin'
    alias_password = 'XXXX%%123xx'

    @staticmethod
    def testOne(query):
        try:
            query.one()
        except:
            return 0
        return 1

    @classmethod
    def testOneOrganization(cls, name = ''):
        if name == '':
            name = cls.orgname
        return cls.testOne(Organization.query.filter_by(full_name = name))


############################################################################
#testdata
def test_create_organizations(client):
    countpre = Organization.query.count()
    expectedcount = countpre + 6
    
    neworg = Organization(full_name='test root org 1', display_name='testorg 1', abbreviation=TAU.org1_abbr)
    db.session.add(neworg)
    newsub1 = Organization(full_name='test sub org 1.1', display_name='testorg 1.1', abbreviation='testorg1.1', parent_org=neworg)
    db.session.add(newsub1)
    
    neworg = Organization(full_name='test root org 2', display_name='testorg 2', abbreviation=TAU.org2_abbr)
    db.session.add(neworg)
    newsub1 = Organization(full_name='test sub org 2.1', display_name='testorg 2.1', abbreviation='testorg2.1', parent_org=neworg)
    db.session.add(newsub1)

    neworg = Organization(full_name='test root org 3', display_name='testorg 3', abbreviation='testorg3')
    db.session.add(neworg)
    newsub1 = Organization(full_name='test sub org 3.1', display_name='testorg 3.1', abbreviation=TAU.org31_abbr, parent_org=neworg)
    db.session.add(newsub1)
    newsub2 = Organization(full_name='test sub org 3.2', display_name='testorg 3.2', abbreviation='testorg3.2', parent_org=neworg)
    db.session.add(newsub1)

    db.session.commit()

    assert Organization.query.count() == expectedcount, 'Failed to insert test organizations'

    org = Organization.query.filter_by(display_name='testorg 1').one()
    assert org, 'organization not found.'
    assert Organization.query.filter_by(parent_org_id=org.id).first()


def test_create_rootuser(client):
    assert User.query.filter_by(_name=TAU.rootuser_name).first() == None, 'test broken. User found via query before insert.'

    newuser = User(name=TAU.rootuser_name)
    newuser.email = TAU.rootuser_email
    newuser.password = TAU.rootuser_password
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'TestTitel.'
    newuser.origin = 'testDS'
    db.session.add(newuser)

    org = Organization.query.filter_by(abbreviation=TAU.org1_abbr).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=newuser,
        membership_role=admin_role)
    db.session.add(oxu)

    db.session.commit()

    #test queries user
    user = User.query.filter_by(_name=TAU.rootuser_name).first()
    assert user, 'User not found via query'
    assert OrganizationMembership.query.filter_by(user_id=user.id).count() == 1, 'No Memberships found for user_id'
    assert OrganizationMembership.query.filter_by(user=user).count() == 1, 'No Memberships found for user object'

    #test user authenticate
    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert len(admin.get_users()) == 1, 'wrong number of users'


def test_create_aliasuser(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).first()

    alias = user.create_alias_user()
    org = Organization.query.filter_by(abbreviation=TAU.org2_abbr).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=alias,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.commit()

    alias = user.create_alias_user()
    org = Organization.query.filter_by(abbreviation=TAU.org31_abbr).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=alias,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.commit()
    
    assert User.query.filter_by(alias_user_id=user.id).count() == 2, 'wrong count for testalias'


def test_get_organizations(client):
    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert admin.get_organizations().count() == 5, 'wrong number of organizations for user'


def test_get_organizations_deleted(client):
    suborg = Organization.query.filter_by(abbreviation='testorg1.1').one()
    suborg.mark_as_deleted()
    db.session.commit()

    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert admin.get_organizations().count() == 4, 'wrong number of organizations for user'


@pytest.mark.skip(reason='test not yet implemented.')
def test_get_memberships(client):
    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert admin.get_memberships().count() == 4, 'wrong number of organizations for user'


@pytest.mark.skip(reason='test not yet implemented.')
def test_get_organizations_raw(client):
    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    multitree = admin.get_organizations_raw()


@pytest.mark.skip(reason='delete system is not yet discussed. test doesnt work.')
def test_get_organizations_for_deleted_alias(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).first()
    alias = User.query.filter_by(alias_user_id=user.id).first()
    alias.mark_as_deleted()

    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert admin.get_organizations().count() == 2, 'Falsche Anzahl Organizations zum neuen User'




