from .conftest import assert_msg
from app.models import User, Organization, OrganizationMembership, MembershipRole, Domain
from app import db
import pytest
import datetime


#################################################################
# Test DS
class TDS:
    org1 = 'testdomain_org1'
    domain1 = 'domain1.at'

    @staticmethod
    def getOrganization(orgname):
        org = Organization.query.filter_by(abbreviation=orgname).first()
        if not org:
            org = Organization(full_name=orgname, display_name=orgname, abbreviation=orgname)
            db.session.add(org)
            db.session.commit()
        return org


#################################################################

def test_create_domain(client):
    org = TDS.getOrganization(TDS.org1)
    assert org, 'test broken. organization not found'

    newdomain = Domain(domain_name=TDS.domain1, organization=org)
    db.session.add(newdomain)
    db.session.commit()
    assert newdomain, 'domain not created'

    domain = Domain.query.filter_by(_domain_name=TDS.domain1).first()
    assert domain, 'domain created but not found by domain_name.'
    domain = Domain.query.filter_by(organization_id=org.id).first()
    assert domain, 'domain created but not found by organization_id.'


def test_mark_as_deleted_organization(client):
    org = Organization.query.filter_by(abbreviation=TDS.org1, deleted=0).first()
    assert org, 'test broken. organization not found'

    domains = Domain.query.filter_by(organization_id=org.id, deleted=0)
    assert domains.count() > 0, 'test broken. no domains found for organization'

    org.mark_as_deleted()
    db.session.commit()
    domains = Domain.query.filter_by(organization_id=org.id, deleted=0)
    assert domains.count() == 0, 'domains not marked as deleted'




