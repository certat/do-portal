from .conftest import assert_msg
from app.models import User, Organization, OrganizationMembership, MembershipRole
from app import db
import pytest
import datetime


class App:
    @property
    def user(self):
        return self.__user

    username = 'Testuser under EnergyOrg Admin'


#namen fuer Test Alias User
class TAU:
    orgname = 'Test alias user-Organization'
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



################################################################################
# test data
def test_create_organization(client):
    neworg = Organization(full_name=TAU.orgname, display_name=TAU.orgname)
    neworg.abuse_emails=['org@test.alias.user']
    db.session.add(neworg)
    db.session.commit()
    assert Organization.query.filter_by(full_name = TAU.orgname).first(), 'Organization not inserted.'
    assert TAU.testOneOrganization(), 'Organization exists multible times'


# test data
def test_create_rootuser(client):
    assert User.query.filter_by(_name=TAU.rootuser_name).first() == None, 'test broken. User found via query before insert.'

    newuser = User(name=TAU.rootuser_name)
    newuser.email = TAU.rootuser_email
    newuser.password = TAU.rootuser_password
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'TestTitle.'
    newuser.origin = 'testdata'
    db.session.add(newuser)

    org = Organization.query.filter_by(full_name = TAU.orgname).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=newuser,
        membership_role=admin_role)
    db.session.add(oxu)

    db.session.commit()

    user = User.query.filter_by(_name=TAU.rootuser_name).first()
    assert user, 'User not found via query'
    assert OrganizationMembership.query.filter_by(user_id=user.id).count() == 1, 'No Memberships found for user_id'
    assert OrganizationMembership.query.filter_by(user=user).count() == 1, 'No Memberships found for user object'

    (admin, auth) = User.authenticate(TAU.rootuser_email, TAU.rootuser_password)
    assert auth is True, 'User cant log in'
    assert len(admin.get_users()) == 1, 'wrong number of users'
    assert admin.get_organizations().count() == 1, 'wrong number of organizations for user'


#test: insert existing user
#expected: Exception
def test_create_rootuser_double(client):
    with pytest.raises(Exception):
        newuser = User(name=TAU.rootuser_name)
        newuser.email = TAU.rootuser_email
        newuser.password = TAU.rootuser_password
        db.session.add(newuser)
        db.session.commit()


#test: user having empty passwd
#expected: Exception
def test_create_rootuser_wrong_passwd(client):
    with pytest.raises(Exception):
        newuser = User(name='test no passwd')
        newuser.email = TAU.rootuser_email
        db.session.add(newuser)
        db.session.commit()


#test: user having empty name
#expected: Exception
def test_create_rootuser_empty_name(client):
    with pytest.raises(Exception):
        newuser = User()
        newuser.email = TAU.rootuser_email
        newuser.password = TAU.rootuser_password
        db.session.add(newuser)
        db.session.commit()


#test: user having empty email
#expected: allowed (because of alias)
def test_create_rootuser_empty_email(client):
    created = True
    try:
        newuser = User(name='test no email')
        newuser.password = TAU.rootuser_password
        db.session.add(newuser)
        db.session.commit()
    except:
        created = False
    assert created, 'User not inserted with empty email'

