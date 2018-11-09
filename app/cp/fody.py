from flask import g, request
from flask_jsonschema import validate
from app.core import ApiResponse
from app import db
from app.fody_models import FodyOrganization
from . import cp


@cp.route('/ripe/handle/<string:ripe_org_hdl>', methods=['GET'])
def get_cp_ripe_handle(ripe_org_hdl):
    try:
        fody_org = FodyOrganization(ripe_org_hdl)
        return ApiResponse(fody_org.__dict__)
    except AttributeError as ae:
        return ApiResponse({'message': str(ae) ,}, 404, {})
