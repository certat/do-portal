from .conftest import assert_msg
from app.models import User, Organization, OrganizationMembership, MembershipRole, Domain
from app import db
import pytest
import datetime


#################################################################
# Test DS
class TDS:
    org1 = 'testdomain_org1'
    org2 = 'testdomain_org2'
    orgwrong = 'testdomain_org_wrongdomain'
    domain1 = 'domain1.at'
    domain2 = 'domain2.at'
    domainwrong = ' '

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

    domain = Domain.query.get(newdomain.id)
    assert domain, 'domain created but not found with get'
    domain = Domain.query.filter_by(_domain_name=TDS.domain1).first()
    assert domain, 'domain created but not found by domain_name'
    domain = org.domains.filter_by(_domain_name=TDS.domain1).first()
    assert domain, 'domain created but not found by organization_id'
    orgtest = domain.organization
    assert org.id == orgtest.id, 'organization not found by Domain.organization'


def test_create_existing_domain(client):
    org = TDS.getOrganization(TDS.org1)
    assert org, 'test broken. organization not found'

    exception_occured = False
    try:
        newdomain = Domain(domain_name=TDS.domain1, organization=org)
        db.session.add(newdomain)
        db.session.commit()
    except:
        db.session.rollback()
        exception_occured = True
    assert exception_occured, 'existing domain created'

    count = Domain.query.filter_by(_domain_name=TDS.domain1, organization_id=org.id).count()
    assert count == 1, 'domain doesnt exist or exists multiple times.'


def test_create_wrong_domain(client):
    org = TDS.getOrganization(TDS.orgwrong)
    assert org, 'test broken. organization not found'

    exception_occured = False
    try:
        newdomain = Domain(domain_name=TDS.domainwrong, organization=org)
        db.session.add(newdomain)
        db.session.commit()
    except:
        db.session.rollback()
        exception_occured = True

    assert exception_occured or newdomain, 'wrong domain created'

    domain = Domain.query.filter_by(_domain_name=TDS.domainwrong).first()
    assert not domain, 'wrong domain created'
    domain = org.domains.first()
    assert not domain, 'wrong domain found by organization.'
    db.session.rollback()


def test_mark_as_deleted_organization(client):
    org = Organization.query.filter_by(abbreviation=TDS.org1, deleted=0).first()
    assert org, 'test broken. organization not found'
    assert org.domains.count() > 0, 'test broken. no domains found for organization'
    count_not_org_domains = Domain.query.filter(Domain.organization_id != org.id).count()
    assert count_not_org_domains != 0, 'test broken. no domains of other organizations found'

    org.mark_as_deleted()
    db.session.add(org)
    db.session.commit()
    # organization should not be selected, when deleted=1 (FilteredQuery)
    o = Organization.query.filter_by(abbreviation=TDS.org1).first()
    assert not o, 'test broken. organization found after mark_as_deleted.'
    domains = Domain.query.filter_by(organization_id=org.id)
    assert domains.count() == 0, 'domains not deleted while organization.mark_as_deleted'
    assert org.domains.count() == 0, 'domains not deleted while organization.mark_as_deleted'
    assert count_not_org_domains == Domain.query.filter(Domain.organization_id != org.id).count(),\
            'domains of other organizations possibly deleted'


def test_delete_domain(client):
    org = TDS.getOrganization(TDS.org2)
    assert org, 'test broken. organization not found'

    newdomain = Domain(domain_name=TDS.domain2, organization=org)
    db.session.add(newdomain)
    db.session.commit()
    assert newdomain, 'test broken. domain not created'

    domain = org.domains.filter_by(_domain_name=TDS.domain2).one()
    assert domain, 'test broken. Domain not found'
    domain.delete()
    db.session.commit()

    domain = Domain.query.filter_by(_domain_name=TDS.domain2).first()
    assert not domain, 'domain deleted, but found by domain_name.'
    domain = org.domains.first()
    assert not domain, 'domain deleted but found by organization.'

