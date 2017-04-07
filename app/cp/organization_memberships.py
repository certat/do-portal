from flask import g, request, abort, url_for
from flask_jsonschema import validate
from app import db
from app.models import OrganizationMembership, Organization, User
from app.api.decorators import json_response
from . import cp


@cp.route('/organization_memberships', methods=['GET'])
@json_response
def get_cp_organization_memberships():
    """Return current_user's organization memberships

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/organization_memberships HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "organization_memberships": [
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
    :resheader Content-Type: This depends on `Accept` header or request

    :>json array organizations: List of available organization membership objects

    For organization details: :http:get:`/api/1.0/organization_memberships/(int:org_id)`

    :status 200: Organization memberships endpoint found, response may be empty
    :status 404: Not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    memberships = g.user.get_organization_memberships()
    return {'organization_memberships': [m.serialize() for m in memberships]}


@cp.route('/organization_memberships/<int:membership_id>', methods=['GET'])
@json_response
def get_cp_organization_membership(membership_id):
    """Return organization membership identified by ``membership_id``

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

    :param org_id: Organization membership unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Organization membership unique ID
    :>json integer role_id: Unique ID of the membership role
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
    membership = OrganizationMembership.query.get_or_404(membership_id)
    check_membership_permissions(membership)
    return membership.serialize()

@cp.route('/organization_memberships', methods=['POST'])
@validate('organization_memberships', 'add_cp_organization_membership')
@json_response
def add_cp_organization_membership():
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
    :resheader Content-Type: This depends on `Accept` header or request

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
    :>json integer id: Organization membership ID

    :status 200: Organization details were successfully updated
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    membership = OrganizationMembership.fromdict(request.json)
    check_membership_permissions(membership)
    db.session.add(o)
    db.session.commit()
    return {'organization_membership': membership.serialize(),
            'message': 'Organization membership added'}, 201, \
           {'Location': url_for('cp.get_cp_organization', membership_id=membership.id)}


@cp.route('/organization_memberships/<int:membership_id>', methods=['PUT'])
@validate('organization_memberships', 'update_cp_organization_membership')
@json_response
def update_cp_organization_membership(membership_id):
    """Update organization membership details

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
    :resheader Content-Type: This depends on `Accept` header or request

    :<json integer role_id: Unique ID of the membership role
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
    membership = OrganizationMembership.query.filter(
        OrganizationMembership.id == membership_id
    ).first()
    if not o:
        return redirect(url_for('cp.add_cp_organization'))
    check_membership_permissions(membership)
    membership.from_json(request.json)
    db.session.add(o)
    db.session.commit()
    return {'message': 'Organization membership saved'}


@cp.route('/organization_memberships/<int:membership_id>', methods=['DELETE'])
@json_response
def delete_cp_organization_membership(membership_id):
    """Delete organization membership

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
          "message": "Organization membership deleted"
        }

    :param org_id: Unique ID of the organization

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: Organization membership was deleted
    :status 404: Organization membership was not found
    """
    membership = OrganizationMembership.query.filter(
        OrganizationMembership.id == membership_id
    ).first_or_404()
    membership.mark_as_deleted()
    db.session.add(membership)
    db.session.commit()
    return {'message': 'Organization membership deleted'}


def check_membership_permissions(membership):
    """ The current user must be able to admin both the membership's
    organization and its user.
    """
    org = Organization.query.get_or_404(membership.org_id)
    user = Organization.query.get_or_404(membership.user_id)
    if not g.user.may_handle_organization(org):
        abort(403)
    if not g.user.may_handle_user(user):
        abort(403)

