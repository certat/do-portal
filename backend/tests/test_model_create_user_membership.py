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
    ciso_role = MembershipRole.query.filter_by(name = 'CISO').one()

    user_dict = {'name': 'testi 123', 
                 'email': 'asasd@asdasd1232.at', 
                 'password': 'Aasda%%asdd12',
                 'birthdate': '1999-09-09',
                 }

    (user, message) = User.create(user_dict)
    db.session.commit()
    assert user.id, 'User id set'
    assert message == 'User added', 'correct message'

    (user_alias, message) = User.create(user_dict)
    db.session.commit()
    assert user_alias.id, 'User id set'
    assert user_alias.alias_user_id, 'User alias id set'
    assert message == 'User aliased', 'correct message'

    organization_membership_dict = {'email': 'somemail@asdasd.com',
                                    'phone': '+43234234234', 
                                    'role_id': ciso_role.id,
                                    'organization_id': org.id,
                                    'user_id': user.id,}
                                    
    (organization_membership, message) = \
          OrganizationMembership.upsert(organization_membership_dict)
    db.session.commit()

    assert organization_membership.user_id == user.id, 'correct user set'
    assert organization_membership.user.name == 'testi 123', 'user name set'
    assert organization_membership.organization.full_name == org_name2, 'user name set'
 
