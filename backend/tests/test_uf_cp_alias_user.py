from flask import url_for
from app.models import User, Organization, OrganizationMembership, MembershipRole
from .conftest import assert_msg
import pytest

class TAU:
    testnewuser_email = 'test@new.user'

    @staticmethod
    def adminuser():
        email='cert@master.at'
        user = User.query.filter_by(_email=email).one()
        assert user, 'test broken. admin user not found'
        return user

    def adminrole():
        name = 'OrgAdmin'
        role = MembershipRole.query.filter_by(name=name).first()
        assert role, 'test broken. admin role not found'
        return role

    @staticmethod
    def rootuser():
        email='admin@eorg.at'
        user = User.query.filter_by(_email=email).one()
        assert user, 'test broken. root user not found'
        return user

    @staticmethod
    def testorg():
        abbr = 'eorg-gas'
        org = Organization.query.filter_by(abbreviation=abbr).one()
        assert org, 'test broken. test organization not found'
        return org

    @classmethod
    def allorgs(cls, org):
        orgs = []
        orgs.append(org.abbreviation)
        for o in org.child_orgs:
            orgs.extend(cls.allorgs(o))
        return orgs

    @classmethod
    def orgs4user(cls, user):
        orgs = list()
        for om in user.user_memberships:
            orgs.extend(cls.allorgs(om.organization))
        return orgs


    @staticmethod
    def firstalias():
        alias = User.query.filter_by(alias_user_id=TAU.rootuser().id).first()
        assert alias, 'test broken. root user not found'
        return alias
        
    @staticmethod
    def top_organization():
        pass

###########################################################


def test_create_aliasuser(client):
    count_om = OrganizationMembership.query.count()
    expectedcount_om = count_om + 1
    count_u = User.query.count()
    expectedcount_u = count_u + 1

    client.api_user = TAU.adminuser()
    testuser = TAU.rootuser()
    testorg = None
    for org in client.api_user.get_organizations().all():
        if not testorg and not org.abbreviation == 'cert' and not testuser.get_organizations().from_self().filter_by(id=org.id).first():
            testorg = org

    expected_abbreviations = TAU.orgs4user(TAU.rootuser())
    #assert expected_abbreviations == []
    #assert TAU.allorgs(testorg) == []
    expected_abbreviations.extend(TAU.allorgs(testorg))

    rv = client.post(
        url_for('cp.add_cp_user'),
        json=dict(
            user=dict(email=testuser.email,
                      name=testuser.name),
            organization_membership=dict(
                membership_role_id=TAU.adminrole().id,
                organization_id=testorg.id,
                email='test@alias.membership')
        )
    )
    assert_msg(rv, value='User aliased;Membership created/updated', response_code=201)

    aliasid = rv.json['user']['id']
    alias = User.get(aliasid)
    assert alias.alias_user_id != None, 'No alias returned'

    assert expectedcount_om == OrganizationMembership.query.count(), 'after insert new alias: wrong count of memberships'
    assert expectedcount_u == User.query.count(), 'after insert new alias: wrong count of users'
    assert 1 == OrganizationMembership.query.filter_by(user_id=aliasid).count(), 'after insert new alias: wrong count of alias-memberships'
    
    client.api_user = TAU.rootuser()
    rv = client.get(
        url_for('cp.get_cp_organizations')
    )
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    got_abbreviations = [i['abbreviation'] for i in got[0]]
    got_abbreviations.sort()

    expected_abbreviations.sort()
    assert got_abbreviations == expected_abbreviations


@pytest.mark.skip(reason='not yet implemented/discussed')
def test_create_existing_alias(client):
    count_om = OrganizationMembership.query.count()
    expectedcount_om = count_om 
    count_u = User.query.count()
    expectedcount_u = count_u

    client.api_user = TAU.adminuser()

    testuser = TAU.rootuser()
    #alias = User.query.filter_by(alias_user_id=TAU.rootuser().id).first()
    #assert alias, 'test broken. no alias found'
    alias = TAU.firstalias()
    om = OrganizationMembership.query.filter_by(membership_role_id=TAU.adminrole().id, user_id=alias.id).first()
    assert om, 'test broken.'
    testorg = Organization.query.filter_by(id=om.organization_id).one()
    assert testorg, 'test broken.'

    rv = client.post(
        url_for('cp.add_cp_user'),
        json=dict(
            user=dict(email=testuser.email,
                      name=testuser.name),
            organization_membership=dict(
                membership_role_id=TAU.adminrole().id,
                organization_id=testorg.id,
                email='test@alias.membership')
        )
    )
    assert rv.status_code != 201, 'after insert existing alias: OK status'
    assert expectedcount_om == OrganizationMembership.query.count(), 'after insert new alias: wrong count of memberships'
    assert expectedcount_u == User.query.count(), 'after insert new alias: wrong count of users'


def test_get_user_memberships(client):
    client.api_user = TAU.rootuser()
    rv = client.get(
        url_for('cp.get_cp_organizations')
    )
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    got_abbreviations = [i['abbreviation'] for i in got[0]]
    got_abbreviations.sort()

    expected_abbreviations = TAU.orgs4user(TAU.rootuser())
    expected_abbreviations.extend(TAU.orgs4user(TAU.firstalias()))
    expected_abbreviations.sort()
    assert got_abbreviations == expected_abbreviations


def test_update_aliasuser_email(client):
    wrongemail = 'test@wrong.alias.email'
    client.api_user = TAU.adminuser()
    aliasid = User.query.filter(User.alias_user_id != None).first().id
    assert aliasid, 'test broken. no aliasid found'

    rv = client.put(
         url_for('cp.update_cp_user', user_id=aliasid),
         json=dict(email=wrongemail,
                   name='wrong alias',
                   password='Bla12345%'
         )
    )
    assert rv.status_code != 200, 'status OK for changing alias email'
    assert User.query.filter_by(_email=wrongemail).count() == 0, 'alias found for changed email'


#@pytest.mark.skip(reason='has to be implemented in model. failure during mark_as_deleted, cause: nonvalid email set')
def test_mark_as_deleted_aliasuser(client):
    expected_orgs = [o.abbreviation for o in TAU.rootuser().get_organizations().all()]
    #assert expected_orgs == []
    to_delete = [o.abbreviation for o in TAU.firstalias().get_organizations().all()]
    #assert to_delete == []
    for abbr in to_delete:
        expected_orgs.remove(abbr)
    #assert expected_orgs == []
    expected_orgs.sort()

    client.api_user = TAU.adminuser()
    alias = TAU.firstalias()
    rv = client.delete(
        url_for('cp.delete_cp_user', user_id=alias.id)
    )
    assert_msg(rv, value='User deleted', response_code=200)

    result = [o.abbreviation for o in TAU.rootuser().get_organizations().all()]
    result.sort()
    assert result == expected_orgs, 'number of organizations after delete not correct'

    client.api_user = TAU.rootuser()
    rv = client.get(
        url_for('cp.get_cp_organizations')
    )
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    result = [i['abbreviation'] for i in got[0]]
    result.sort()
    assert result == expected_orgs, 'number of organizations after delete not correct ia API'

    for om in alias.user_memberships:
        assert om.deleted == 1, 'membership has not been deleted while delete of alias'
        assert om.organization.deleted == 0, '[possibly no error] organization is deleted'


@pytest.mark.skip(reason="requirements for delete must o be discussed first")
def test_mark_as_deleted_rootuser(client):
    pass


#test: creating alias from alias through update alias_user_id of rootuser
#@pytest.mark.skip(reason='has to be implemented. possible error.')
def test_update_alias_user_id(client):
    #testdata
    client.api_user = TAU.adminuser()
    testorg = Organization.query.filter(Organization.abbreviation != 'cert').first()
    assert testorg, 'test broken. no organization found'

    rv = client.post(
        url_for('cp.add_cp_user'),
        json=dict(
            user=dict(email='test@newuser.becomes.alias',
                      name='test newuser update to alias'),
                      #password='Bla12345%'),
            organization_membership=dict(
                membership_role_id=TAU.adminrole().id,
                organization_id=TAU.testorg().id,
                email='test2@alias.membership')
        )
    )
    assert_msg(rv, value='User added;Membership created/updated', response_code=201)

    userid = rv.json['user']['id']
    user = User.get(userid)
    assert user, 'test broken. user not found'

    rv = client.put(
         url_for('cp.update_cp_user', user_id=user.id),
         json=dict(alias_user_id=TAU.rootuser().id,
                   name='Max Muster',
                   password='Bla12345%')
    )
    user = User.get(userid)
    assert user.alias_user_id == None, 'alias_user_id of rootuser has been set'
    assert rv.status_code != 200, 'no error code while alias_user_id of rootuser set'
    assert_msg(rv, value='Attribute update error. update of alias_user_id not allowed', response_code=422)


#test: possible to create an alias of an alias
#cant be implemented while alias_user_id can be updated.
@pytest.mark.skip(reason="test not yet implemented. cause: alias_user_id can be updated.")
def test_create_aliasbyalias(client):
    pass


@pytest.mark.skip(reason="test not yet implemented. cause: requirements not yet discussed.")
def test_authenticate_alias(client):
    pass


@pytest.mark.skip(reason='test not yet implemented. cause: requirements not yet discussed.')
def test_update_aliasuser(client):
    pass


