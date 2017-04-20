from app.models import User, Organization, MembershipRole, \
    OrganizationMembership
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
    username = 'Testuser under Verbund Admin'

    admin = User.query.filter_by(name="Verbund Admin").first()
    assert len(admin.user_memberships) == 3
    org = admin.get_organizations().first()

    c = len(admin.get_users())
    assert c == 3, 'Verbung Admin has 3 users'
    certorg = Organization.query.filter_by(abbreviation='cert').first()

    newuser = User(name=username)
    newuser.password = 'bla'
    db.session.add(newuser)
    db.session.commit()
    assert newuser.id > 0
    assert admin.may_handle_organization(certorg) is False, \
        'verbund admin may not handle cert org'
    assert admin.may_handle_organization(org) is True
    role = MembershipRole.query.filter_by(name='CISO').first()
    oxu = OrganizationMembership(
        phone='4711',
        organization=org,
        user=newuser,
        membership_role=role,
    )
    db.session.commit()
    assert oxu.id > 0, 'OrganizationMembership written'
    assert len(admin.get_users()), 'Verbund Admin now has 4 users'
