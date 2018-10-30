from app.fody_models import FodyOrganization
from app.models import Organization, FodyOrg_X_Organization
from app import db
import datetime
import pytest

# from .conftest import assert_msg
# from app.fixtures import testfixture


def test_fody_organization():
    fody_org = FodyOrganization(ripe_org_hdl = 'ORG-AGNS1-RIPE')
    assert fody_org.ripe_org_hdl == 'ORG-AGNS1-RIPE', 'found ripe handle'
    assert fody_org.name == 'AT&T Global Network Services Nederland B.V.', 'found name'

    with pytest.raises(AttributeError):
        fody_org = FodyOrganization(ripe_org_hdl = 'blablabla')

def test_link_fody_org():
    forg_x_org = FodyOrg_X_Organization();
    certorg = Organization.query.filter_by(abbreviation='cert').first()
    forg_x_org.organization_id = certorg.id
    forg_x_org.ripe_org_hdl = 'ORG-AGNS1-RIPE'
    db.session.add(forg_x_org)
    db.session.commit()
