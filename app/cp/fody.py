from flask import g, request, abort
from flask_jsonschema import validate
from app.core import ApiResponse
from app import db
from app.models import FodyOrganization, Organization, FodyOrg_X_Organization, NotificationSetting
from . import cp
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from requests.utils import unquote


@cp.route('/ripe/handle/<string:ripe_org_hdl>', methods=['GET'])
def get_cp_ripe_handle(ripe_org_hdl):
    try:
        fody_org = FodyOrganization(ripe_org_hdl)
        return ApiResponse(fody_org.__dict__)
    except AttributeError as ae:
        return ApiResponse({'message': str(ae) ,}, 404, {})

@cp.route('/ripe/settings/<int:org_id>/<string:ripe_org_hdl>', methods=['GET'])
def get_cp_settings(ripe_org_hdl, org_id):
    o = Organization.query.get_or_404(org_id)
    if not g.user.may_handle_organization(o):
        abort(403)

    try:
        forg_x_org = FodyOrg_X_Organization.query.filter_by \
             (organization_id=org_id, _ripe_org_hdl=ripe_org_hdl).one();
    except NoResultFound:
        abort(404)

    return ApiResponse(forg_x_org.notification_settings)

@cp.route('/ripe/settings/<int:org_id>/<string:ripe_org_hdl>', methods=['PUT', 'POST'])
def set_cp_settings(ripe_org_hdl, org_id):
    o = Organization.query.get_or_404(org_id)
    if not g.user.may_handle_organization(o):
        abort(403)

    try:
        forg_x_org = FodyOrg_X_Organization.query.filter_by \
             (organization_id=org_id, _ripe_org_hdl=ripe_org_hdl).one();
    except NoResultFound:
        abort(404)

    try:
        setting = request.json

        forg_x_org.upsert_notification_setting(**setting)
        db.session.commit()
    except TypeError as e:
        return ApiResponse({'message': str(e) ,}, 421, {})
    except AttributeError as e:
        return ApiResponse({'message': str(e) ,}, 421, {})

    return ApiResponse({'message': 'Setting added'}, 201, {})

@cp.route('/ripe/contact/<string:cidr>', methods=['GET'])
def get_cp_contact_for_netblock(cidr):
    cidr = unquote(cidr)
    try:
        notification_setting = NotificationSetting.contact_for_netblock(cidr)
    except AttributeError as e:
        return ApiResponse({'message': str(e) ,}, 404, {})
    except Exception as e:
        return ApiResponse({'message': str(e) ,}, 421, {})

    return ApiResponse(notification_setting)

