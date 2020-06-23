from app.models import User, Organization, MembershipRole, \
    OrganizationMembership, Country
from app.models import FodyOrganization
from app import db
import datetime
import pytest
from pprint import pprint

# from .conftest import assert_msg
# from app.fixtures import testfixture


class App:
    @property
    def user(self):
        return self.__user

    username = 'Testuser under EnergyOrg Admin'


def test_create_orgadmin():
    newuser = User(name='test_org admin ')
    newuser.email = 'org_admin_simple@bla.com'
    newuser.password = 'blaBla123%'
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'DDDr. hc. mult.'
    newuser.origin = 'your mother'
    org_name1 = 'energyorg-electricity'
    org_name2 = 'eorg'

    org = Organization.query.filter_by(full_name = org_name2).one()

    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=newuser,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.add(newuser)
    db.session.commit()
    assert newuser.api_key, 'api key is set'

    assert newuser.get_organizations().count() == 3 
    '''
    for uo in newuser.get_organization_memberships():
        print("id {} user_id {} org_id {}".format(uo.id, uo.user_id, uo.organization_id))

    for o in newuser.get_organizations():
        print("id {} org name {}".format(o.id, o.full_name))
    '''    
    # add user as admin on a different branch
    org = Organization.query.filter_by(full_name = org_name1).one()
    oxu = OrganizationMembership(
        organization=org,
        user=newuser,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.add(newuser)
    db.session.commit()
    assert newuser.api_key, 'api key is set'
    
    assert newuser.get_organizations().count() == 5 
    '''
    for o in newuser.get_organizations():
        print("id {} org name {}".format(o.id, o.full_name))
        
    '''
    

'''
def test_create_alias_user():
    u = User.query.filter_by(_name='eorgmaster').first()
    alias_user = u.create_alias_user()
    # print("\n" + alias_user.name + "\n")
    role = MembershipRole.query.filter_by(name='CISO').first()
    energy_org = Organization.query.filter_by(abbreviation='energyorg').one()
    oxu = OrganizationMembership(
        phone='+123214711',
        mobile='+12321312',
        email='asda@ddasd.at',
        organization=energy_org,
        user=alias_user,
        membership_role=role,
        pgp_key_id='asdasdasd',
        pgp_key_fingerprint='ADFEFEF123123',
        pgp_key='asdasasfasfasf',
        smime='asdasdasd',
        coc=b'asasda')
    db.session.add(oxu)
    db.session.commit()
'''


def test_organizations():
    (admin, auth) = User.authenticate('org_admin_simple@bla.com', 'blaBla123%')
    assert auth is True
    # pprint(admin.get_organizations_raw())

    full_names = [org.full_name for org in admin.get_organizations()]
    full_names.sort()
    assert full_names == \
            ['energyorg-electricity',
              'energyorg-electricity-transmission',
              'eorg',
              'eorg-electricity',
              'eorg-gas'] \
          , 'correct list of orgs for energyorg'

def test_organizations_raw():
    (admin, auth) = User.authenticate('org_admin_simple@bla.com', 'blaBla123%')
    assert auth is True
    # pprint(admin.get_organizations_raw())
    assert len(admin.get_organizations_raw()) == 5, 'correct number of org' 
