from app.fody_models import FodyOrganization
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


