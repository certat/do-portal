from flask import g, request, abort, url_for
from flask_jsonschema import validate
from app import db
from app.models import User, OrganizationMembership, Organization, MembershipRole
from app.api.decorators import json_response
from . import cp


@cp.route('/users', methods=['GET'])
@json_response
def get_cp_users():
    """Return current_user's users

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/users HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "users": [
            {
              "id": 25,
              "login": "foo@bar.com",
              "password": "abc123",
              "name": "Max Muster"
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

    :>json array organizations: List of available user objects

    For user details: :http:get:`/api/1.0/users/(int:org_id)`

    :status 200: Users endpoint found, response may be empty
    :status 404: Not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    users = g.user.get_users()
    return {'users': [u.serialize() for u in users]}


@cp.route('/users/<int:user_id>', methods=['GET'])
@json_response
def get_cp_user(user_id):
    """Return user identified by ``user_id``

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/users/44 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "id": 25,
          "login": "foo@bar.com",
          "password": "abc123",
          "login": "Max Muster"
        }

    :param user_id: User unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: User unique ID
    :>json string login: Login email address
    :>json string password: Password
    :>json string name: Name

    :status 200: Returns user details object
    :status 404: Resource not found
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    user = User.query.get_or_404(user_id)
    if not g.user.may_handle_user(user):
        abort(403)
    return user.serialize()

@cp.route('/users', methods=['POST'])
@validate('users', 'add_cp_user')
@json_response
def add_cp_user():
    """Add new user

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/users HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "login": "foo@bar.com",
          "password": "abc123",
          "name": "Max Muster",
          "role_id": 12,
          "organization_id": 201
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "message": "User saved"
        }

    **Example validation error**:

    .. sourcecode:: http

        HTTP/1.0 400 BAD REQUEST
        Content-Type: application/json

        {
          "message": "'name' is a required property",
          "validator": "required"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: This depends on `Accept` header or request

    :<json string login: Login email address. If not present, the user can't
            login
    :<json string password: Password
    :<json string name: Name
    :<json integer role_id: Unique ID of the organization user role
    :<json integer organization_id: Unique ID of the organization

    :>json string message: Status message
    :>json integer id: User ID

    :status 200: User details were successfully saved
    :status 400: Bad request
    :status 401: Authorization failure. The client MAY repeat the request with
        a suitable API-Authorization header field. If the request already
        included Authorization credentials, then the 401 response indicates
        that authorization has been refused for those credentials.
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    """
    role_id = request.json.pop('role_id', None)
    org_id = request.json.pop('organization_id', None)

    user = User.fromdict(request.json)

    # The role and organization must exist and the current user must be able to
    # admin the organization.

    role = MembershipRole.query.get_or_404(role_id)
    org = Organization.query.get_or_404(org_id)
    membership = OrganizationMembership.fromdict({
        'role_id': role_id,
        'organization_id': org_id })
    if not g.user.may_handle_organization(org):
        abort(403)
    db.session.add(user)
    db.session.commit()

    membership.user_id = user.id
    db.session.add(membership)
    db.session.commit()
    return {'user': user.serialize(),
            'message': 'User added'}, 201, \
           {'Location': url_for('cp.get_cp_user', user_id=user.id)}


@cp.route('/users/<int:user_id>', methods=['PUT'])
@validate('users', 'update_cp_user')
@json_response
def update_cp_user(user_id):
    """Update user details

    **Example request**:

    .. sourcecode:: http

        PUT /api/1.0/organizations HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "login": "foo@bar.com",
          "password": "abc123"
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
          "message": "'login' is a required property",
          "validator": "required"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: This depends on `Accept` header or request

    :<json string login: Login email address
    :<json string password: Password
    :<json string name: Name

    :>json string message: Status message

    :status 200: Organization details were successfully updated
    :status 400: Bad request
    :status 422: Validation error
    """
    user = User.query.filter(
        User.id == user_id
    ).first()
    if not user:
        return redirect(url_for('cp.add_cp_user'))
    if not g.user.may_handle_user(user):
        abort(403)
    user.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return {'message': 'User saved'}


@cp.route('/users/<int:user_id>', methods=['DELETE'])
@json_response
def delete_cp_user(user_id):
    """Delete user

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/users/2 HTTP/1.1
        Host: cp.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "User deleted"
        }

    :param org_id: Unique ID of the organization

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: User was deleted
    :status 404: User was not found
    """
    # The user can't delete himself
    if user_id == g.user.id:
        abort(403)
    user = User.query.filter(
        User.id == user_id
    ).first_or_404()
    if not g.user.may_handle_user(user):
        abort(403)
    user.mark_as_deleted()
    db.session.add(user)
    db.session.commit()
    return {'message': 'User deleted'}

