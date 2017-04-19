from app.models import User
# from .conftest import assert_msg
# from app.fixtures import testfixture


def test_model():
    u = User.query.filter_by(name="certmaster").first()

    for uo in u.user_memberships:
        assert uo.email == 'cert@master.at'
        assert uo.organization.full_name == 'Energy CERT Austria'
        cc = 0
        for co in uo.organization.child_organizations:
            cc += 1
        assert cc == 2, 'two child orgs'
    assert u.email == 'cert@master.at'
