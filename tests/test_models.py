from app.models import User, Organization, MembershipRole, \
    OrganizationMembership, Country
from app import db
import datetime
import pytest
# from .conftest import assert_msg
# from app.fixtures import testfixture


class App:
    @property
    def user(self):
        return self.__user

    username = 'Testuser under Verbund Admin'


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
        assert uo.sms_alerting == 1
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
    assert len(u.get_users()) == 7, 'find all subordinate users - once'
    # assert c == 7, 'find all subordinate users - once'


def test_create_user():
    """
    + get user who we know is an admin
    + get org for this user
    + get some other org (certorg)

    + create new user
    + try to
    """

    admin = User.query.filter_by(name="Verbund Admin").first()
    assert len(admin.user_memberships) == 1
    org = admin.get_organizations().first()

    c = len(admin.get_users())
    assert c == 3, 'Verbung Admin has 3 users'
    certorg = Organization.query.filter_by(abbreviation='cert').first()

    newuser = User(name=App.username)
    with pytest.raises(AttributeError):
        newuser.email = 'testbla.com'
    newuser.email = 'test@bla.com'
    newuser.password = 'bla'
    newuser.picture = b'asasda'
    newuser.birthdate = datetime.datetime.utcnow()
    newuser.title = 'DDDr. hc. mult.'
    newuser.origin = 'your mother'
    db.session.add(newuser)
    db.session.commit()
    assert newuser.id > 0
    assert admin.may_handle_organization(certorg) is False, \
        'verbund admin may not handle cert org'
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
            coc=b'asasda'
        )
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
        coc=b'asasda'
    )
    db.session.commit()
    assert oxu.id > 0, 'OrganizationMembership written'
    assert len(admin.get_users()) == 4, 'Verbund Admin now has 4 users'
    App.user = newuser


def test_login():
    # verbundciso is not allowed to login
    (verbundciso, auth) = User.authenticate('cisouser@verbund.at', 'bla')
    assert auth is False

    (admin, auth) = User.authenticate('admin@verbund.at', 'blabla')
    assert auth is True

    new_password = User.reset_password_send_email('admin@verbund.at')
    (admin, auth) = User.authenticate('admin@verbund.at', new_password)
    assert auth is True


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


def test_delete_user():
    assert App.user.name == App.username
    App.user.mark_as_deleted()
    assert App.user.deleted == 1
    assert App.user.ts_deleted
    db.session.commit()
    admin = User.query.filter_by(name="Verbund Admin").first()
    assert len(admin.get_users()) == 3, 'Verbund Admin now has 3 users'
    i = 0
    for um in App.user.user_memberships:
        i += 1
        assert um.deleted == 1, \
            'All memeberships also have to be marked as deleted'
        assert um.ts_deleted <= datetime.datetime.utcnow()
    assert i == 1, 'exactly one membership'
