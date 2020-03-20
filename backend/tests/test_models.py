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


def test_countries_inserted():
    country = Country.query.filter_by(cc='AR').first()
    assert country.name == 'Argentina', 'Dont cry for me Argentina'


def test_user_memberships():
    u = User.query.filter_by(name="certmaster").first()

    for uo in u.user_memberships:
        assert uo.email == 'cert@master.at'
        assert uo.zip == '1010'
        assert uo.city == 'Wien'
        assert uo.street == 'Karlsplatz 1'
        assert uo.mobile == "+3412312312"
        assert uo.organization.full_name == 'Energy CERT Austria'
        assert uo.country.name == 'Austria', 'Country is an object'
        cc = 0
        for co in uo.organization.child_organizations:
            cc += 1
        assert cc == 2, 'two child orgs'
    assert u.email == 'cert@master.at'


def test_get_users():
    u = User.query.filter_by(name="certmaster").first()
    # c = 0
    # for user in u.get_users():
    #    c += 1
    assert len(u.get_users()) == 8, 'find all subordinate users - once'
    # assert c == 7, 'find all subordinate users - once'


def test_create_user():
    """
    + get user who we know is an admin
    + get org for this user
    + get some other org (certorg)

    + create new user
    + try to
    """

    admin = User.query.filter_by(name="EnergyOrg Admin").first()
    assert len(admin.user_memberships) == 1
    org = admin.get_organizations().first()

    c = len(admin.get_users())
    assert c == 3, 'Verbung Admin has 3 users'
    certorg = Organization.query.filter_by(abbreviation='cert').first()

    newuser = User(name=App.username)
    with pytest.raises(AttributeError):
        newuser.email = 'testbla.com'
    newuser.email = 'test@bla.com'
    newuser.password = 'blaBla123%'
    newuser.picture = b'asasda'
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'DDDr. hc. mult.'
    newuser.origin = 'your mother'
    db.session.add(newuser)
    db.session.commit()
    assert newuser.id > 0
    assert admin.may_handle_organization(certorg) is False, \
        'energyorg admin may not handle cert org'
    assert admin.may_handle_organization(org) is True

    role = MembershipRole.query.filter_by(name='CISO').first()
    with pytest.raises(AttributeError):
        oxu = OrganizationMembership(
            phone='+43434711',
            email='asdaddasd.at',
            organization=org,
            user=newuser,
            membership_role=role,
            pgp_key_id='asdasdasd',
            pgp_key_fingerprint='ADFEFEF123123',
            pgp_key='asdasasfasfasf',
            smime='asdasdasd',
            coc=b'asasda')
    oxu = OrganizationMembership(
        phone='+123214711',
        mobile='+12321312',
        email='asda@ddasd.at',
        organization=org,
        user=newuser,
        membership_role=role,
        pgp_key_id='asdasdasd',
        pgp_key_fingerprint='ADFEFEF123123',
        pgp_key='asdasasfasfasf',
        smime='asdasdasd',
        coc=b'asasda')
    db.session.add(oxu)
    db.session.commit()
    assert oxu.id > 0, 'OrganizationMembership written'
    assert len(admin.get_users()) == 4, 'EnergyOrg Admin now has 4 users'
    App.user = newuser


def test_create_orgadmin():
    newuser = User(name='test_org admin ')
    newuser.email = 'org_admin@bla.com'
    newuser.password = 'blaBla123%'
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'DDDr. hc. mult.'
    newuser.origin = 'your mother'

    org = Organization.query.filter_by(full_name = 'eorg').one()

    admin_role = MembershipRole.query.filter_by(name='OrgAdmin').one()
    oxu = OrganizationMembership(
        organization=org,
        user=newuser,
        membership_role=admin_role)
    db.session.add(oxu)
    db.session.add(newuser)
    db.session.commit()
    assert newuser.api_key, 'api key is set'



def test_create_user_with_duplicate_email():
    newuser = User(name=App.username)
    with pytest.raises(ValueError):
        newuser.email = 'test@bla.com'

def test_create_alias_user():
    u = User.query.filter_by(name='eorgmaster').first()
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



def test_login():
    # energyorgciso is not allowed to login
    (energyorgciso, auth) = User.authenticate('cisouser@energyorg.at', 'bla')
    assert auth is False

    (admin, auth) = User.authenticate('admin@energyorg.at', 'blaBla12$')
    assert auth is True

    ''' XXX
    new_password = User.reset_password_send_email('admin@energyorg.at')
    (admin, auth) = User.authenticate('admin@energyorg.at', new_password)
    assert auth is True
    '''

    new_password2 = 'B12blibli%'
    admin.password = new_password2
    (admin, auth) = User.authenticate('admin@energyorg.at', new_password2)
    assert auth is True

    # admin@energyorg has 4 contacts via organization_memberships
    assert admin.get_organization_memberships().count() == 5

    # full_names =
    #     list(map(lambda org: org.full_name, admin.get_organizations()))
    full_names = [org.full_name for org in admin.get_organizations()]
    full_names.sort()
    assert full_names == ['energyorg', 'energyorg-electricity',
                          'energyorg-electricity-transmission',
                          'energyorg-gas'], \
        'correct list of orgs for energyorg'

    '''
def test_organizations_raw():
    (admin, auth) = User.authenticate('admin@energyorg.at', 'blaBla12$')
    assert auth is True
    pprint(admin.get_organizations_raw())

    # full_names = [org.full_name for org in admin.get_organizations()]
    full_names.sort()
    assert full_names == ['energyorg', 'energyorg-electricity',
                          'energyorg-electricity-transmission',
                          'energyorg-gas'], \
        'correct list of orgs for energyorg'
    '''



def test_delete_membership():
    u = User.query.filter_by(name=App.user.name).first()
    with pytest.raises(AttributeError):
        um = u.user_memberships[0]
        um.mark_as_deleted()


def test_update_incorrect_data():
    u = User.query.filter_by(name=App.user.name).first()
    with pytest.raises(AttributeError):
        u.user_memberships[0].phone = '1235455'
    with pytest.raises(AttributeError):
        u.user_memberships[0].mobile = '1235455'
    with pytest.raises(AttributeError):
        u.email = 'somethingwrong'


def test_update_membership_data():
    u = User.query.filter_by(name=App.user.name).first()
    u.user_memberships[0].phone = None
    assert u.user_memberships[0].phone is None, \
        'phone number correctlty set to Null/None'
    u.user_memberships[0].mobile = '+43123124123'
    assert u.user_memberships[0].mobile == '+43123124123', \
        'mobile number correctlty set'


def test_delete_user():
    assert App.user.name == App.username
    App.user.mark_as_deleted()
    assert App.user.deleted == 1
    assert App.user.ts_deleted
    db.session.commit()
    admin = User.query.filter_by(name="EnergyOrg Admin").first()
    assert len(admin.get_users()) == 4, 'EnergyOrg Admin now has 3 users'
    i = 0
    for um in App.user.user_memberships:
        i += 1
        assert um.deleted == 1, \
            'All memeberships also have to be marked as deleted'
        assert um.ts_deleted <= datetime.datetime.utcnow()
    assert i == 1, 'exactly one membership'


# https://domainis.univie.ac.at/mantis/view.php?id=4071
def test_read_org_with_more_admins():
    admin = User.query.filter_by(name="E-Org Gas Admin").first()
    # oms4user = admin.get_organization_memberships()
    # Organization.query.get_or_404(org_id)
    orgs = admin.get_organizations()
    assert [o.full_name for o in orgs] == \
        ['eorg-electricity'], 'correct orgs'
    assert len([o.id for o in orgs]) == 1, 'OrgAdmin for 1  orgs'

def test_delete_organization_with_childs():
    eorg = Organization.query.filter_by(abbreviation='eorg').one()
    assert eorg.full_name == 'eorg';

    eorg_elec = Organization.query.filter_by(abbreviation='eorg-electricity').one()
    eorg_elec.mark_as_deleted()
    db.session.add(eorg_elec)
    db.session.commit()

    for o in eorg.child_organizations:
        assert o.abbreviation == 'eorg-gas'

    with pytest.raises(AttributeError):
        eorg.mark_as_deleted()

def test_delete_unused_users():
    count = User.delete_unused_users()
    print("*** {}".format(count))

'''
def test_organization_notification_settings():
    eorg = Organization.query.filter_by(abbreviation='eorg').one()
    eorg.ripe_handles = ['ORG-AGNS1-RIPE', 'ORG-AAPA1-RIPE']
    db.session.add(eorg)
    db.session.commit()

    for eorg_ripe_org in eorg.ripe_organizations:
        print(FodyOrganization(eorg_ripe_org.ripe_org_hdl).asns)
'''        
