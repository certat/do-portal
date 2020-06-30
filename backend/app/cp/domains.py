from flask import g, abort, request, url_for
from flask_jsonschema import validate
from app.core import ApiResponse
from app import db, app
from app.models import Organization, Permission, User, Domain
from app.api.decorators import permission_required
from . import cp
import psycopg2
import sqlalchemy.exc
import os


@cp.route('/organizations/<int:organization_id>/domains', methods=['GET'])
def get_cp_organization_domains(organization_id):
    """
    :status 200: Domain endpoint found, response may be empty
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 404: Not found
    """
    org = Organization.query.get_or_404(organization_id)
    if org.deleted:
        abort(404)
    if not g.user.may_handle_organization(org):
        abort(401)
    return ApiResponse({'domains': [d.serialize() for d in org.domains.order_by(Domain._domain_name.asc())]})


@cp.route('/domains/<int:domain_id>', methods=['GET'])
def get_cp_domain(domain_id):
    """
    :status 200: Domain endpoint found, response may be empty
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 404: Not found
    """
    domain = Domain.query.get_or_404(domain_id)
    if not domain:
        abort(404)

    #org = Organization.get(domain.organization_id)
    org = domain.organization
    if not org:
        abort(404)
    if not g.user.may_handle_organization(org):
        abort(401)
    return ApiResponse(domain.serialize())


@cp.route('/domains', methods=['POST'])
@validate('domains', 'add_cp_domain')
def add_cp_domain():
    """
    :status 201: Domain details were successfully inserted
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 422: Validation error.
    """
    domain = Domain.fromdict(request.json)
    if not (domain and domain.organization_id and domain.domain_name):
        abort(400)

    org = Organization.query.get(domain.organization_id)
    if not org:
        abort(404)
    if not g.user.may_handle_organization(org):
        abort(401)

    try:
        db.session.add(domain)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as ie:
        db.session.rollback()
        if isinstance(ie.orig, psycopg2.errors.UniqueViolation):
            return ApiResponse({'message': 'already exists' ,}, 422, {})
        else:
            return ApiResponse({'message': str(ie.orig) ,}, 422, {})
    except Exception as e:
        db.session.rollback()
        return ApiResponse({'message': str(e) ,}, 400, {})

    return ApiResponse({'domain': domain.serialize(),
            'message': 'Domain added'}, 201, \
           {'Location': url_for('cp.get_cp_domain', domain_id=domain.id)})


@cp.route('/domains/<int:domain_id>', methods=['PUT'])
@validate('domains', 'update_cp_domain')
def update_cp_domain(domain_id):
    """
    :status 200: Domain details were successfully updated
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.

    :status 422: Validation error.
    """
    domain = Domain.query.get_or_404(domain_id)
    if not domain:
        abort(404)
    if not domain.organization_id:
        return ApiResponse({'message': 'domain has no organization'}, 403, {})
 
    #org = Organization.query.filter(Organization.id == domain.organization_id).first()
    org = domain.organization
    if not org:
        return ApiResponse({'message': 'organization doesnt exist'}, 400, {})
    if not g.user.may_handle_organization(org):
        abort(401)

    untouchables_ = ['organization_id']
    for k in untouchables_:
        request.json.pop(k, None)

    try:
        domain.from_json(request.json)
    except:
        return ApiResponse({'message': 'could not update'}, 421, {})

    try:
        db.session.add(domain)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as ie:
        db.session.rollback()
        if isinstance(ie.orig, psycopg2.errors.UniqueViolation):
            return ApiResponse({'message': 'already exists' ,}, 422, {})
        else:
            return ApiResponse({'message': str(ie.orig) ,}, 422, {})
    except:
        db.session.rollback()
        db.session.refresh
        return ApiResponse({'message': 'could not update'}, 421, {})
    return ApiResponse({'message': 'Domain saved'})


@cp.route('/domains/<int:domain_id>', methods=['DELETE'])
def delete_cp_domain(domain_id):
    """
    :status 200: Domain successfully deleted
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 404: Not found
    :status 422: Validation error.
    """
    domain = Domain.query.get_or_404(domain_id)
    if not domain:
        abort(404)
    if not domain.organization_id:
        return ApiResponse({'message': 'domain has no organization'}, 403, {})

    org = domain.organization
    if not org:
        return ApiResponse({'message': 'organization doesnt exist'}, 400, {})
    if not g.user.may_handle_organization(org):
        abort(401)

    try:
        domain.delete()
    except AttributeError as ae:
        return ApiResponse({'message': str(ae) ,}, 422, {})
    except Exception as e:
        return ApiResponse({'message': str(e) ,}, 422, {})

    try:
        db.session.commit()
    except Exception as e:
        return ApiResponse({'message': str(e) ,}, 422, {})

    return ApiResponse({'message': 'Domain deleted'})

