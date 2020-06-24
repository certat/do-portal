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
    if not g.user.may_handle_organization(org):
        abort(401)
    return ApiResponse({'domains': [d.serialize() for d in org.domains]})


@cp.route('/domains/<int:domain_id>', methods=['GET'])
def get_cp_domain(domain_id):
    """Return domain identified by ``domain_id``

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/domain/44 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
        }

    :param domain_id: domain unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Domain unique ID
    :>json string domain_name: Name of domain
    :>json integer organization_id: organization ID

    :status 200: Domain endpoint found, response may be empty
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 404: Not found"""
    domain = Domain.query.get_or_404(domain_id)
    if domain:
        org = Organization.get(domain.organization_id)
        if not org:
            abort(404)
        if not g.user.may_handle_organization(org):
            abort(401)
    return ApiResponse(domain.serialize())


@cp.route('/domains', methods=['POST'])
@validate('domains', 'add_cp_domain')
def add_cp_domain():
    """Add new domain
    When adding a new domain an organization id is required.

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/domains HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json
        {
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json
        {
        }

    **Example validation error**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
        }

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :<json string domain_name: Domain Name of organization
    :<json integer organization_id: Unique ID of the belonging organization
    :>json integer id: domain ID

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
# @permission_required(Permission.ORGADMIN)
def update_cp_domain(domain_id):
    """Update domain details

    **Example request**:

    .. sourcecode:: http

        PUT /api/1.0/domains HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json
        Content-Type: application/json
        {
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "message": "Domain saved"
        }

    **Example validation error**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json
        {
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json integer id: Unique ID of domain
    :<json string domain_name: Domain name of organization
    :<json integer organization_id: Unique ID of the belonging organization

    :status 200: Domain details were successfully updated
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 422: Validation error."""
    domain = Domain.query.filter(Domain.id == domain_id).first()
    if not domain:
        return redirect(url_for('cp.add_cp_domain'))
    if not domain.organization_id:
        return ApiResponse({'message': 'domain has no organization'}, 403, {})
    org = Organization.query.filter(Organization.id == domain.organization_id).first()
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
    """Delete domain

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/domains/2 HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Domain deleted"
        }

    :param domain_id: Unique ID of the domain

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

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
    domain = Domain.query.filter(Domain.id == domain_id).first_or_404()
    if not domain:
        return redirect(url_for('cp.add_cp_domain'))
    if not domain.organization_id:
        return ApiResponse({'message': 'domain has no organization'}, 403, {})
    org = Organization.query.filter(Organization.id == domain.organization_id).first()
    if not org:
        return ApiResponse({'message': 'organization doesnt exist'}, 400, {})

    if not g.user.may_handle_organization(org):
        abort(401)

    try:
        #domain.mark_as_deleted()
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

