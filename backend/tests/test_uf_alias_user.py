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


#test: create alias user
def test_create_aliasuser(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'User not found.'
    countalias = User.query.filter_by(alias_user_id=user.id).count()
    countexpected = countalias + 1
    
    alias_user = user.create_alias_user()
    assert User.query.filter_by(alias_user_id=user.id).count() == countexpected, 'Alias user not inserted.'


#test: mark_as_deleted rootuser
@pytest.mark.skip(reason="requirements for delete are to be discussed/implemented first")
def test_mark_as_deleted_rootuser(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'User not found.'

    user.mark_as_deleted()
    db.session.commit()
    assert User.query.filter_by(alias_user_id=user.id).count() > 0, 'Test broken. no aliases for user'

    for um in user.user_memberships:
        assert um.deleted == 1, 'User Membership of rootuser not marked as deleted.'

    for alias in user.aliased_users:
        assert alias.deleted == 1, 'Alias not marked as deleted.'
        for um in alias.user_memberships:
            assert um.deleted == 1, 'User Membership of alias not marked as deleted.'


#test: delete rootuser
@pytest.mark.skip(reason="requirements for delete are to be discussed first")
def test_delete_rootuser_with_aliases(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'test broken. User not found.'
    
    alias = user.aliased_users[0]
    assert alias, 'test broken. No alias found for user.'

    aid = alias.id
    with pytest.raises(AttributeError):
        User.query.filter_by(_name=TAU.rootuser_name).delete()
    db.session.rollback()


#test: update rootuser name.
#expected: old username not found.
#expected: name of alias user returns '#' + updated name of rootuser
@pytest.mark.skip(reason='changes in models possible. test must be updated before test')
def test_update_rootuser_name(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'test broken. User not found.'
    user.name = TAU.rootuser_updatedname
    db.session.add(user)
    db.session.commit()

    updateduser = User.query.filter_by(_name=TAU.rootuser_updatedname).one()
    olduserexists =  TAU.testOne(User.query.filter_by(_name=TAU.rootuser_name))
    assert updateduser and not olduserexists, 'User not updated'
 
    for aliasuser in updateduser.aliased_users:
        assert aliasuser.name == '#' + updateduser.name, 'Name of alias user not updated.'


#reset test data for further tests
def test_reset_name(client):
    user = User.query.filter_by(_name=TAU.rootuser_updatedname).first()
    if user:
        user.name = TAU.rootuser_name
        db.session.add(user)
        db.session.commit()

    updateduser = User.query.filter_by(_name=TAU.rootuser_name).one()
    olduserexists =  TAU.testOne(User.query.filter_by(_name=TAU.rootuser_updatedname))
    assert updateduser and not olduserexists, 'Could not reset updated user'


#test: update email of alias
#expected: empty email for alias user
@pytest.mark.skip(reason='must be implemented first')
def test_update_aliasuser_email(client):
    testemail = 'test@email.alias.user'
    assert User.query.filter_by(_email=testemail).first() == None, 'test broken. test email found before test.'
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'Test broken. user not found.'
    #if no users left from previous tests
    if User.query.filter_by(alias_user_id=user.id).count() == 0:
        aliasuser = user.create_alias_user()
        db.session.commit()
    alias = User.query.filter_by(alias_user_id=user.id).first()
    assert alias, 'test broken. alias user not found.'
    
    with pytest.raises(AttributeError):
        alias.email = testemail
        db.session.add(testuser)
        db.session.commit()
    assert User.query.filter_by(_email = testemail).first() == None, '[security] email of alias could be set and was not empty after that.'


#test: mark as deleted for alias
@pytest.mark.skip(reason='requirements for delete are to be discussed first')
def test_mark_as_deleted_aliasuser(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'User not found.'

    alias = user.create_alias_user()
    assert user, 'alias not found.'
    
    org = Organization.query.filter_by(full_name = TAU.orgname).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=alias,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.commit()

    try:
        alias.mark_as_deleted()
        db.session.commit()
    except:
        db.session.rollback()
        assert False, 'Test not possible. unexpected exception!'

    assert User.query.filter_by(alias_user_id=user.id).count() > 0, 'Test not possible, no aliases for user'

    for um in alias.user_memberships:
        assert alias.deleted == 1, 'User Membership of alias not marked as deleted'


#Delete des aliasuser
@pytest.mark.skip(reason='requirements for delete are to be discussed first')
def test_delete_aliasuser(client):
    user = User.query.filter_by(_name=TAU.rootuser_name).one()
    assert user, 'test broken. User not found.'

    alias = user.create_alias_user()
    assert user, 'test broken. alias not found.'

    org = Organization.query.filter_by(full_name = TAU.orgname).one()
    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=alias,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.commit()

    assert OrganizationMembership.query.filter_by(user_id=alias.id).count() > 0, 'OrganizationMembership for alias was not created'

    #exception fur test not important.
    try:
        User.query.filter_by(id=alias.id).delete()
        db.session.commit()
    except:
        db.session.rollback()

    assert User.query.filter_by(id=alias.id).count() == 0, 'alias has not been deleted'

    assert OrganizationMembership.query.filter_by(user_id=alias.id).count() == 0, 'OrganizationMembership not deleted, when alias user of that membership was deleted.'
    

#test: login with alias
#expected: not authenticated
def test_authenticate_alias(client):
    query = User.query.filter_by(alias_user_id=None)
    assert query.count() > 0, 'test not possible. no aliases found'
    for alias in query.all():
        if OrganizationMembership.query.filter_by(user_id=alias.id).count() == 0:
            org = Organization.query.filter_by(full_name = TAU.orgname).one()
            admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
            oxu = OrganizationMembership(
                organization=org,
                user=alias,
                membership_role=admin_role)
            db.session.add(oxu)
            db.session.commit()
    (alias, auth) = User.authenticate(None, TAU.alias_password)
    assert auth == False, '[security] authenticate possibe for alias.'
    assert alias == None, '[security] authenticate possibe for alias.'
    (alias, auth) = User.authenticate('', TAU.alias_password)
    assert auth == False, '[security] authenticate possibe for alias.'
    assert alias == None, '[security] authenticate possibe for alias.'


#test: updates of alias
@pytest.mark.skip(reason='test not yet implemented. cause: requirements not yet discussed.')
def test_update_aliasuser(client):
    pass



