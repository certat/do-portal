from flask import g, request, abort, url_for
from flask_jsonschema import validate
from app.core import ApiResponse
from app import db
from app.models import User, OrganizationMembership, Organization, MembershipRole
from . import cp


@cp.route('/users', methods=['GET'])
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
              "name": "Max Muster",
              "picture": "image/png;base64,iVBORw0KGgoAAAANS...",
              "birthdate": "1951-03-22",
              "title": "Dr.",
              "origin": "Uranus"
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

    For user details: :http:get:`/api/1.0/users/(int:user_id)`

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
    return ApiResponse({'users': [u.serialize(exclude=('picture')) for u in users]})


@cp.route('/users/<int:user_id>', methods=['GET'])
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
          "login": "Max Muster",
          "picture": "image/png;base64,iVBORw0KGgoAAAANS...",
          "birthdate": "1951-03-22",
          "title": "Dr.",
          "origin": "Uranus"
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
    :>json string picture: Base64-encoded PNG profile picture
    :>json string birthdate: Birthdate as YYYY-MM-DD
    :>json string title: Academic or honorific title
    :>json string origin: Origin

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
    return ApiResponse(user.serialize())

@cp.route('/users/<int:user_id>/memberships', methods=['GET'])
def get_cp_users_memberships(user_id):
    """Return user identified by ``user_id``

    **Example request**:

    .. sourcecode:: http

        GET /cp/1.0/users/44/memberships HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "memberships": [
            {
              "city": "Wien",
              "country": {
                "cc": "AT",
                "id": 10,
                "name": "Austria"
              },
              "country_id": 10,
              "email": "proschinger@energy-cert.at",
              "id": 53,
              "membership_role_id": 2,
              "mobile": "+436649650926",
              "organization_id": 3,
              "phone": null,
              "street": "Karlsplatz 1/2/9",
              "user_id": 58,
              "zip": "1010"
            },
            {
              "email": "christian.proschinger@nic.at",
              "id": 173,
              "membership_role_id": 15,
              "mobile": "+436649650922",
              "organization_id": 30,
              "phone": null,
              "user_id": 58
            },
            {
              "email": "security@nic.at",
              "id": 174,
              "membership_role_id": 5,
              "mobile": "+436649650922",
              "organization_id": 30,
              "phone": "+436649650922",
              "user_id": 58
            }
          ]
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
    :>json string picture: Base64-encoded PNG profile picture
    :>json string birthdate: Birthdate as YYYY-MM-DD
    :>json string title: Academic or honorific title
    :>json string origin: Origin

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
    memberships = user.get_memberships()
    return ApiResponse({'memberships': [m.serialize(exclude=('coc', 'smime')) for m in memberships]})


@cp.route('/users/<int:user_id>/memberships/<int:membership_id>', methods=['GET'])
def get_cp_users_memberships_by_id(user_id, membership_id):

    user = User.query.get_or_404(user_id)
    if not g.user.may_handle_user(user):
        abort(403)
    memberships = user.get_memberships(membership_id)
    return ApiResponse(memberships)



@cp.route('/users', methods=['POST'])
@validate('users', 'add_cp_user')
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
          "picture": "image/png;base64,iVBORw0KGgoAAAANS...",
          "birthdate": "1951-03-22",
          "title": "Dr.",
          "origin": "Uranus",
          "membership_role_id": 12,
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
    :<json string picture: Base64-encoded PNG profile picture
    :<json string birthdate: Birthdate as YYYY-MM-DD
    :<json string title: Academic or honorific title
    :<json string origin: Origin
    :<json integer membership_role_id: Unique ID of the organization user role
    :<json integer organization_id: Unique ID of the organization
    :<json string country_id: Unique ID of the country
    :<json string street: Street address
    :<json string zip: Zip code
    :<json string phone: Phone number
    :<json string email: Email address
    :<json string comment: Arbitrary comment
    :<json string pgp_key_id: PGP key ID
    :<json string pgp_key_fingerprint: PGP key fingerprint
    :<json string pgp_key: PGP key
    :<json string smime: S/MIME
    :<json string coc: Code of Conduct

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
    try:
        (user, user_create_message) = User.create(request.json['user'])
    except AttributeError as ae:
        return ApiResponse({'message': 'Attribute error. Invalid email, phone or mobile?' + str(ae) ,}, 422, {})
    db.session.commit()

    # The role and organization must exist and the current user must be able to
    # admin the organization.
    request_membership = request.json['organization_membership']
    request_membership['user_id'] = user.id
    org = Organization.query.get_or_404(request_membership['organization_id'])
    role_id = request_membership['membership_role_id']
    role = MembershipRole.query.get_or_404(role_id)

    if not g.user.may_handle_organization(org):
        abort(403)

    (membership, om_message) = \
        OrganizationMembership.upsert(request_membership) 
    db.session.commit()
    return ApiResponse({'user': user.serialize(),
            'organization_membership': membership.serialize(),
            'message': user_create_message + ';' + om_message
           }, 201, \
           {'Location': url_for('cp.get_cp_user', user_id=user.id)})


@cp.route('/users/<int:user_id>', methods=['PUT'])
@validate('users', 'update_cp_user')
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
    :<json string picture: Base64-encoded PNG profile picture
    :<json string birthdate: Birthdate as YYYY-MM-DD
    :<json string title: Academic or honorific title
    :<json string origin: Origin

    :>json string message: Status message

    :status 200: Organization details were successfully updated
    :status 400: Bad request
    :status 422: Validation error
    """
    user = User.query.filter(
        User.id == user_id
    ).first()

    if user.alias_user_id:
        return ApiResponse({'message': 'User is an aliased user and may not be updated'}, 422, {})

    if not user:
        return redirect(url_for('cp.add_cp_user'))
    if not g.user.may_handle_user(user):
        abort(403)

    if 'alias_user_id' in request.json and request.json['alias_user_id'] != user.alias_user_id:
        return ApiResponse({'message': 'Attribute update error. update of alias_user_id not allowed',}, 422, {})

    try:
        user.from_json(request.json)
    except AttributeError as ae:
        return ApiResponse({'message': 'Attribute update error. Invalid email, phone or mobile? ' + str(ae),}, 422, {})

    try:
        if 'password' in request.json:
            user.password = request.json['password']
            if user != g.user:
                user.reset_password_send_email(user.email)
            db.session.add(user)
            db.session.commit()
    except AttributeError as ae:
        return ApiResponse({'message': str(ae)}, 422, {})
    db.session.add(user)
    db.session.commit()
    return ApiResponse({'message': 'User saved'})


@cp.route('/users/<int:user_id>', methods=['DELETE'])
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

    :param user_id: Unique ID of the user

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
    return ApiResponse({'message': 'User deleted'})
