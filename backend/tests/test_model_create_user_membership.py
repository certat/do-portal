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


def test_create_user():
    org_name2 = 'eorg'

    org = Organization.query.filter_by(full_name = org_name2).one()

    user_dict = {'name': 'test', 
                 'email': 'asasd@asdasd1232.at', 
                 'password': 'Aasda%%asdd12',
                 'birthdate': '1999-09-09',
                 }

    (user, message) = User.create(user_dict)
    db.session.commit()
    assert user.id, 'User id set'
    assert message == 'User added', 'correct message'
    print(user.id, message)

    (user_alias, message) = User.create(user_dict)
    db.session.commit()
    assert user_alias.id, 'User id set'
    assert user_alias.alias_user_id, 'User alias id set'
    assert message == 'User aliased', 'correct message'
    print(user_alias.id, message)

