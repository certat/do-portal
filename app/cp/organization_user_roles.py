from flask import g, request
from flask_jsonschema import validate
from app import db
from app.models import MembershipRole
from app.api.decorators import json_response
from . import cp


@cp.route('/organization_user_roles', methods=['GET'])
@json_response
def get_cp_organization_user_roles():
    """Return organization user roles

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/organization_user_roles HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "organization_user_roles": [
            {
              "id": 2,
              "name": "abuse-c",
              "display_name" : "Domain Abuse Contact (abuse-c)"
            },
            {
              "id": 3,
              "name": "billing-c",
              "display_name" : "Domain Billing Kontakt (billing-c)"
            },
          ]
        }

    **Example error response**:

    .. sourcecode:: http

        HTTP/1.0 404 NOT FOUND
        Content-Type: application/json

        {
          "message": "Resource not found",
          "status": "not found"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json array organizations: List of available organization user role objects

    For details: :http:get:`/api/1.0/organization_user_roles/(int:org_id)`

    :status 200: Organization user roles endpoint found, response may be empty
    :status 404: Not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    roles = MembershipRole.query.all()
    return {'organization_user_roles': [r.serialize() for r in roles]}


@cp.route('/organization_user_roles/<int:role_id>', methods=['GET'])
@json_response
def get_cp_organization_user_role(role_id):
    """Return organization user role identified by ``org_id``

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/organization_user_roles/12 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "id": 2,
          "name": "abuse-c",
          "display_name" : "Domain Abuse Contact (abuse-c)"
        },

    :param role_id: organization user role unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Organization user role unique ID
    :>json string name: Role name
    :>json string display_name: Role display name

    :status 200: Returns organization user role details object
    :status 404: Resource not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    r = MembershipRole.query.get_or_404(role_id)
    return r.serialize()
