from flask import url_for
from app.models import User, Organization, OrganizationMembership, MembershipRole
from app import db
from .conftest import assert_msg
import pytest

#namen fuer Test Alias User
class TAU:
    '''
    org1_abbr = 'testorg1'
    org2_abbr = 'testorg2'
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


    @staticmethod
    def get_top_organization_id():
        try:
            org = Organization.query.filter_by(parent_org_id=None, abbreviation='cert').one()
        except:
            assert False, 'Top organization: not found or exists multiple times'
        return org.id

    @staticmethod
    def get_org_id_per_abbr(abbreviation):
        try:
            org = Organization.query.filter_by(abbreviation=abbreviation).one()
        except:
            assert False, 'Top organization: not found or exists multiple times'
        return org.id

    @staticmethod
    def find_user_by_name(name):
        return User.query.filter_by(_name=name).first()
    '''

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
        abbr = 'energyorg'
        org = Organization.query.filter_by(abbreviation=abbr).one()
        assert org, 'test broken. test organization not found'
        return org

    def testsuborg():
        abbr = 'energyorg-gas'
        org = Organization.query.filter_by(abbreviation=abbr).one()
        assert org, 'test broken. test sub organization not found'
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

#########################################################################

def test_data_create_suborg_membership(client):
    client.api_user = TAU.adminuser()
    rv = client.post(
        url_for('cp.add_cp_user'),
        json=dict(
            user=dict(email=TAU.rootuser().email,
                      name=TAU.rootuser().name),
            organization_membership=dict(
                membership_role_id=TAU.adminrole().id,
                organization_id=TAU.testsuborg().id,
                email='test@alias.membership')
        )
    )
    assert_msg(rv, value='User aliased;Membership created/updated', response_code=201)

    aliasid = rv.json['user']['id']
    assert aliasid != None, 'No alias returned'
    alias = User.get(aliasid)
    assert alias != None, 'alias doesnt exist'
    assert alias.alias_user_id != None, 'returned user is no alias'
    assert OrganizationMembership.query.filter_by(user_id=alias.id).first(), 'alias has no memberships'


@pytest.mark.skip('not yet implemented/discussed')
def test_mark_as_deleted_organization(client):
    client.api_user = TAU.rootuser()
    rv = client.get(
        url_for('cp.get_cp_organizations')
    )
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    orgs_expected = [i['abbreviation'] for i in got[0]]
    orgs_expected.remove(TAU.testsuborg().abbreviation)
    orgs_expected.sort()

    try:
        suborg = TAU.testsuborg()
        suborg.mark_as_deleted()
        db.session.add(suborg)
        db.session.commit()
    except:
        assert False, 'test broken. sub org has not been deleted.'

    rv = client.get(
        url_for('cp.get_cp_organizations')
    )
    assert_msg(rv, key='organizations')
    got = list(rv.json.values())
    orgs = [i['abbreviation'] for i in got[0]]
    orgs.sort()
    assert orgs == orgs_expected, 'organization not removed properly.'

    assert User.query.filter_by(alias_user_id=TAU.rootuser().id, deleted=0).count() == 0, 'expected, that alias_user with deleted memberships is deleted himself'
    

#test: alias must be marked as deleted, when last membership ist marked as deleted.
@pytest.mark.skip('test not yet implemented')
def test_delete_alias_automatically(client):
    pass


@pytest.mark.skip('test not yet implemented')
def test_mark_as_deleted_suborganization(client):
    pass


@pytest.mark.skip('test not yet implemented')
def test_mark_as_deleted_membership(client):
    pass


@pytest.mark.skip('test not yet implemented')
def test_visible_roles(client):
    pass


@pytest.mark.skip('test not yet implemented')
def test_update_alias_membership(client):
    pass

