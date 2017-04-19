from app.models import User, Organization
from app import db
# from .conftest import assert_msg
# from app.fixtures import testfixture


def test_user_memberships():
    u = User.query.filter_by(name="certmaster").first()

    for uo in u.user_memberships:
        assert uo.email == 'cert@master.at'
        assert uo.organization.full_name == 'Energy CERT Austria'
        cc = 0
        for co in uo.organization.child_organizations:
            cc += 1
        assert cc == 2, 'two child orgs'
    assert u.email == 'cert@master.at'


def test_get_users():
    u = User.query.filter_by(name="certmaster").first()
    c = 0
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
    assert len(admin.user_memberships) == 3
    org = admin.get_organizations().first()

    certorg = Organization.query.filter_by(abbreviation='cert').first()

    username = 'Testuser under Verbund Admin'
    newuser = User(name=username)
    newuser.password = 'bla'
    db.session.add(newuser)
    db.session.commit()
    assert newuser.id > 0
    assert admin.may_handle_organization(certorg) is False
    assert admin.may_handle_organization(org) is True
