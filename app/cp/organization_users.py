from flask import g, request
from flask_jsonschema import validate
from app import db
from app.models import OrganizationUser, Organization, User
from app.api.decorators import json_response
from . import cp


@cp.route('/organization_users', methods=['GET'])
@json_response
def get_cp_organization_users():
    """Return current_user's organization memberships

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/organization_users HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "organization_users": [
            {
              "id": 25,
              "role_id": 12,
              "user_id": 153,
              "organization_id": 201,
              "country": "Austria",
              "street": "Mustergasse 2/4",
              "zip": "1234",
              "phone": "+4315671234",
              "email": "max@muster.at",
              "comment": "foo"
            }
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

    :>json array organizations: List of available organization membership objects

    For organization details: :http:get:`/api/1.0/organization_users/(int:org_id)`

    :status 200: Organizations endpoint found, response may be empty
    :status 404: Not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    orgs = g.user.organization_users
    return {'organization_users': [o.serialize() for o in orgs]}


@cp.route('/organization_users/<int:org_user_id>', methods=['GET'])
@json_response
def get_cp_organization_user():
    """Return organization membership identified by ``org_user_id``

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/organization/44 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "id": 25,
          "role_id": 12,
          "user_id": 153,
          "organization_id": 201,
          "country": "Austria",
          "street": "Mustergasse 2/4",
          "zip": "1234",
          "phone": "+4315671234",
          "email": "max@muster.at",
          "comment": "foo"
        }

    :param org_id: organization membership unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Organization membership unique ID
    :>json integer role_id: Unique ID of the organization user role
    :>json integer user_id: Unique ID of the user
    :>json integer organization_id: Unique ID of the organization
    :>json string country: Country name
    :>json string street: Street address
    :>json string zip: Zip code
    :>json string phone: Phone number
    :>json string email: Email address
    :>json string comment: Arbitrary comment

    :status 200: Returns organization membership details object
    :status 404: Resource not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    org_user = OrganizationUser.query.get_or_404(org_user_id)
    check_org_user_permissions(org_user)
    return org_user.serialize()

@cp.route('/organization_users', methods=['POST'])
@validate('organization_users', 'add_cp_organization_user')
@json_response
def add_cp_organization_user():
    """Add new organization membership

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/organizations HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "role_id": 12,
          "user_id": 153,
          "organization_id": 201,
          "country": "Austria",
          "street": "Mustergasse 2/4",
          "zip": "1234",
          "phone": "+4315671234",
          "email": "max@muster.at",
          "comment": "foo"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "message": "Organization saved"
        }

    **Example validation error**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
          "message": "'abbreviation' is a required property",
          "validator": "required"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :<json integer role_id: Unique ID of the organization user role
    :<json integer user_id: Unique ID of the user
    :<json integer organization_id: Unique ID of the organization
    :<json string country: Country name
    :<json string street: Street address
    :<json string zip: Zip code
    :<json string phone: Phone number
    :<json string email: Email address
    :<json string comment: Arbitrary comment

    :>json string message: Status message
    :>json integer id: Organization user membership ID

    :status 200: Organization details were successfully updated
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    org_user = OrganizationUser.fromdict(request.json)
    check_org_user_permissions(org_user)
    db.session.add(o)
    db.session.commit()
    return {'organization_user': org_user.serialize(),
            'message': 'Organization user membership added'}, 201, \
           {'Location': url_for('cp.get_cp_organization', org_user_id=org_user.id)}


@cp.route('/organization_users/<int:org_user_id>', methods=['PUT'])
@validate('organization_users', 'update_cp_organization_user')
@json_response
def update_cp_organization_user():
    """Update organization user membership details

    **Example request**:

    .. sourcecode:: http

        PUT /api/1.0/organizations HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "role_id": 12,
          "user_id": 153,
          "organization_id": 201,
          "country": "Austria",
          "street": "Mustergasse 2/4",
          "zip": "1234",
          "phone": "+4315671234",
          "email": "max@muster.at",
          "comment": "foo"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "message": "Organization saved"
        }

    **Example validation error**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
          "message": "'abbreviation' is a required property",
          "validator": "required"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json integer role_id: Unique ID of the organization user role
    :<json integer user_id: Unique ID of the user
    :<json integer organization_id: Unique ID of the organization
    :<json string country: Country name
    :<json string street: Street address
    :<json string zip: Zip code
    :<json string phone: Phone number
    :<json string email: Email address
    :<json string comment: Arbitrary comment

    :>json string message: Status message

    :status 200: Organization details were successfully updated
    :status 400: Bad request
    :status 422: Validation error
    """
    org_user = OrganizationUser.query.filter(
        OrganizationUser.id == org_user_id
    ).first()
    if not o:
        return redirect(url_for('cp.add_cp_organization'))
    check_org_user_permissions(org_user)
    org_user.from_json(request.json)
    db.session.add(o)
    db.session.commit()
    return {'message': 'Organization user membership saved'}


@cp.route('/organization_users/<int:org_user_id>', methods=['DELETE'])
@json_response
def delete_cp_organization_user(org_user_id):
    """Delete organization user membership

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/organizatoin_users/2 HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Organization user membership deleted"
        }

    :param org_id: Unique ID of the organization

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: Organization user membership was deleted
    :status 404: Organization user membership was not found
    """
    org_user = OrganizationUser.query.filter(
        OrganizationUser.id == org_user_id
    ).first_or_404()
    org_user.mark_as_deleted()
    db.session.add(org_user)
    db.session.commit()
    return {'message': 'Organization user membership deleted'}


def check_org_user_permissions(org_user):
    """ The current user must be able to admin both the membership's
    organization and its user.
    """
    org = Organization.query.get_or_404(org_user.org_id)
    user = Organization.query.get_or_404(org_user.user_id)
    if not org.is_user_allowed(g.user):
        abort(403)
    if not user.is_user_allowed(g.user):
        abort(403)

