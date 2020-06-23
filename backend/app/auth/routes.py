import os
import random
import binascii
import pyqrcode
from io import BytesIO
from flask import request, current_app, render_template
from flask import flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_jsonschema import validate
from app.models import User, Role, ContactEmail, Permission, Organization
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature
from . import auth
from app.core import ApiResponse, ApiException
from app.utils.mail import send_email
from app.api.decorators import permission_required
from app.api.decorators import json_response
from app.utils import bosh_client
from .forms import SetPasswordForm


@auth.route('/login', methods=['POST'])
def login():
    """Authenticate users

    To authenticate make a JSON POST request with credentials.
    On success the API will return a ``rm`` cookie valid for 48 hours.
    Use the value of the ``rm`` cookie for all subsequent requests.
    The ``CP-TOTP-Required`` header notifies clients that they need to submit
    their 2FA token. Token will be check at :http:post:`/auth/verify-totp`

    .. note::

        2FA is used for CP requests only

    **Example request**:

    .. sourcecode:: http

        POST /auth/login HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "email": "some@mail.com",
          "password":"test"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Set-Cookie: rm=.eGwfP...; Expires=Sun, 29-Nov-2015 09:11:45 GMT; Path=/
        Set-Cookie: session=.eJwlzrs...; Secure; HttpOnly; Path=/

        {
          "auth": "authenticated"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request
    :resheader Set-Cookie: Pass the `rm` cookie to future requests
    :resheader CP-TOTP-Required: When true client must submit TOTP at
      :http:post:`/auth/verify-totp`

    :<json string email: Email or username
    :<json string password: Password
    :>json string auth: Authentication status

    :statuscode 200: Login successful
    :statuscode 401: Invalid credentials
    """
    if current_user.is_authenticated:
        return ApiResponse({'auth': 'authenticated'})

    email = request.json.get('email') or request.json.get('username')
    password = request.json.get('password')

    if email and password:
        cp_host = request.environ.get('HTTP_HOST', None)
        if cp_host.startswith('cp.'):
            user, authenticated = User.authenticate(email, password)
            if user and authenticated:
                if user.otp_enabled:
                    session['cu'] = email
                    session['cpasswd'] = password
                    return ApiResponse({'auth': 'pre-authenticated'},
                                       200,
                                       {'CP-TOTP-Required': user.otp_enabled})
                else:
                    if login_user(user, remember=True):
                        return ApiResponse({'auth': 'authenticated'})

            raise ApiException('Invalid username or password', 401)

        if current_app.config['LDAP_AUTH_ENABLED']:
            return do_ldap_authentication(email, password)

        user, authenticated = User.authenticate(email, password)
        if user and authenticated:
            if login_user(user, remember=True):
                return ApiResponse({'auth': 'authenticated',  
                        'logout_inactive_seconds': current_app.config['LOGOUT_INACTIVE_SECONDS']})

    raise ApiException('Invalid username or password', 401)


@auth.route('/verify-totp', methods=['POST'])
@validate('auth', 'verify_totp')
def verify_totp():
    """Check the `TOTP
    <https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm>`_
    submitted by the client.

    **Example request**:

    .. sourcecode:: http

        POST /auth/verify-totp HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "totp": "123456"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Set-Cookie: session=40e418c37cb4cc68_5776d7a0; Secure; HttpOnly; Path=/
        Set-Cookie: rm=.eJwNzrEKAjEMANB_OW4USZqkTW_SwcnFQUQQhzZtUPQ44f4fvPVN7z
          Gsy9wPc3l_97bMw2741U_zMK2vIhgmBMAx8f10vh5vchmLdLS;
          Expires=Sun, 03-Jul-2016 20:52:58 GMT; Secure; HttpOnly; Path=/

        {
          "auth": "authenticated"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request
    :resheader Set-Cookie: Pass the `rm` cookie to future requests

    :<json integer totp: 6 digit authentication code generated by one of these
      TOTP applications: `Google Authenticator
      <https://support.google.com/accounts/answer/1066447?hl=en>`_,
      `Duo Mobile <https://guide.duo.com/third-party-accounts>`_,
      `Authenticator <https://www.microsoft.com/en-US/store/apps/
      Authenticator/9WZDNCRFJ3RJ>`_
    :>json string auth: Authentication status

    :status 200: Login successful
    :status 404: User doesn't have 2FA enabled
    :status 401: User did not provide the first authentication factor
    :status 400: Invalid TOTP
    """
    email = session.pop('cu', None)
    password = session.pop('cpasswd', None)
    user, authenticated = User.authenticate(email, password)
    if not authenticated:
        raise ApiException('Please login first', 401)

    token = request.json['totp']
    user = User.query.filter_by(id=user.id).first_or_404()
    if not user.otp_enabled:
        raise ApiException('Verification failed', 400)

    if user.verify_totp(token):
        if login_user(user, remember=True):
            return ApiResponse({'auth': 'authenticated'})

    raise ApiException('Authentication code verification failed', 400)


@auth.route('/logout')
@login_required
def logout():
    """Logout users

    **Example request**:

    .. sourcecode:: http

        GET /auth/logout HTTP/1.1
        Host: do.cert.europa.eu
        Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Set-Cookie: rm=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Max-Age=0;
          Path=/
        Set-Cookie: session=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Max-Age=0;
          Path=/

        {
          "logged_out": "true"
        }

    :resheader Content-Type: this depends on `Accept` header or request
    :resheader Set-Cookie: Resets ``session`` and ``rm`` cookies

    :>json string logged_out: Logout status

    :statuscode 200: logout successful
    """
    logout_user()
    headers = {}
    return ApiResponse({'logged_out': 'true'}, 200, headers)


@auth.route('/register', methods=['POST'])
@validate('auth', 'register_cp_account')
@login_required
@permission_required(Permission.ADDCPACCOUNT)
def register():
    """Register new constituent account

    .. note::

        The email address will be added to :class:`~app.models.Email` and
        :attr:`~app.models.ContactEmail.cp` will be enabled.

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/auth/register HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

        {
          "organization_id": 317,
          "name": "BEREC (user@domain.tld)",
          "email": "user@domain.tld"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "message": "User registered. An activation email was sent to ..."
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer organization_id: Organization unique ID
    :>json string name: Name of account
    :>json string email: E-mail address

    :status 201: Account created.
    """
    org = Organization.query.filter_by(id=request.json['organization_id']).\
        first_or_404()
    eml = ContactEmail.query.filter_by(
        email=request.json['email'],
        organization_id=request.json['organization_id']).first()
    if not eml:
        eml = ContactEmail.fromdict(request.json)
    eml.cp = True

    user = User.fromdict(request.json)
    user.password = _random_ascii()
    user.api_key = user.generate_api_key()
    if org.is_sla:
        roles = Role.query.filter(db.not_(Role.permissions == 0xff)).all()
        for role in roles:
            if ((role.permissions & Permission.SLAACTIONS) ==
                    Permission.SLAACTIONS):
                user.role = role
                break
    db.session.add(user)
    db.session.add(eml)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        raise e
    expiry = 72 * 3600
    activation_token = user.generate_reset_token(expiry)
    send_email('Your account details', [user.email],
               'auth/email/activate_account', user=user,
               webroot=current_app.config['CP_WEB_ROOT'],
               token=activation_token, expiry=expiry / 60)
    msg = 'User registered. An activation email was sent to {}'
    return ApiResponse({'message': msg.format(user.email)}, 201)


@auth.route('/unregister', methods=['POST'])
@validate('auth', 'unregister_cp_account')
@login_required
@permission_required(Permission.ADDCPACCOUNT)
def unregister():
    """Unregister CP account

    User will be removed from :class:`app.models.User` and
    :attr:`~app.models.ContactEmail.cp` will be disabled.

    .. note::

        The email address will NOT be deleted from :class:`~app.models.Email`.

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/auth/unregister HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

        {
          "organization_id": 317,
          "name": "BEREC (user@domain.tld)",
          "email": "user@domain.tld"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "User has been unregistered. A notification has been..."
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer organization_id: Organization unique ID
    :>json string name: Name of account
    :>json string email: E-mail address

    :status 200: Account has been unregistered.
    """
    eml = ContactEmail.query.filter_by(
        email=request.json['email'],
        organization_id=request.json['organization_id']).first()
    eml.cp = False
    db.session.add(eml)

    user = User.query.filter_by(email=request.json['email']).first()
    send_email('Your account details', [user.email],
               'auth/email/deactivate_account', user=user)
    notify = user.email
    User.query.filter_by(email=request.json['email']).delete()
    db.session.commit()
    msg = 'User has been unregistered. A notification has been sent to {}'
    return ApiResponse({'message': msg.format(notify)})


@auth.route('/account')
@login_required
def account():
    """Return account information

    **Example request**:

    .. sourcecode:: http

        GET /auth/account HTTP/1.1
        Host: do.cert.europa.eu
        Content-Type: application/json

    **Example success response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "api_key": "V3lKallXeGxlRUJqWlhKMExtVjFjbTl3WVM1bGRTSXNJa3hFUVZBVs",
          "email": "dummy@cert.europa.eu",
          "name": "Big dummy"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string api_key: API key
    :>json string email: E-mail
    :>json string name: Full name

    :statuscode 200:
    :statuscode 401: Unauthorized
    """
    return ApiResponse(current_user.serialize())


@auth.route('/change-password', methods=['POST'])
@validate('auth', 'change_password')
def change_password():
    """Change password

    **Example request**:

    .. sourcecode:: http

        POST /auth/change-password HTTP/1.1
        Host: do.cert.europa.eu
        Content-Type: application/json

        {
          "current_password": "123456",
          "new_password": "12345678",
          "confirm_password": "12345678"
        }

    **Example success response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 31

        {
          "message": "Password updated"
        }

    **Example error response**:

    .. sourcecode:: http

        HTTP/1.0 422 UNPROCESSABLE ENTITY
        Content-Type: application/json
        Content-Length: 87

        {
          "message": "'current_password' is a required property",
          "validator": "required"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json string current_password: Current password
    :<json string new_password: New password
    :<json string confirm_password: Password confirmation
    :>json string message: Action status

    :statuscode 200: Password successfully changed
    :statuscode 422: Unprocessable Entity.
    """
    if not current_user.check_password(request.json.get('current_password')):
        raise ApiException('Invalid current password')
    # it makes no sense to check the current password
    # if not current_user.check_password(request.json.get('current_password')):
    #    return {'message': 'Invalid current password'}, 400
    new_pass = request.json.get('new_password', None)
    confirm_pass = request.json.get('confirm_password', None)
    if new_pass != confirm_pass:
        raise ApiException('Confirmation password does not match')
    try:
        current_user.password = request.json.get('new_password')
        db.session.add(current_user)
        db.session.commit()
        return ApiResponse({'message': 'Your password has been updated'})
    except AssertionError as ae:
        raise ApiException(ae)
# uses new ApiException has to uses in the portal as well
#        return {'message': str(ae)}
#    except AttributeError as ae:
#        return {'message': str(ae)}


@auth.route('/reset-api-key')
@login_required
def reset_api_key():
    current_user.api_key = current_user.generate_api_key()
    db.session.add(current_user)
    db.session.commit()
    return ApiResponse({'message': 'Your API key has been reset'})

@auth.route('/lost_password', methods=['POST'])
@validate('users', 'lost_password')
def lost_password():
    """Request a new password

    **Example request**:

    .. sourcecode:: http

        POST /iauth/lost_password HTTP/1.1
        Accept: application/json
        Content-Type: application/json

        {
          "email": "foo@bar.com"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "message": "Password sent"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :reqheader API-Authorization: API key. If present authentication and
            authorization will be attempted.
    :resheader Content-Type: This depends on `Accept` header or request

    :<json string email: Email address for which to reset the password

    :>json string message: Status message

    :status 200: Password restore email was successfully sent
    :status 400: Bad request
    :status 403: Access denied. Authorization will not help and the request
        SHOULD NOT be repeated.
    :status 422: There was a problem with sending the email
    """
    try:
        User.reset_password_send_email(request.json['email'])
    except AttributeError:
        return ApiResponse({'message': 'Attribute error. Invalid email?',}, 422, {})
    return ApiResponse({'message': 'Password restore email sent'})


@auth.route('/activate-account', methods=['POST'])
def set_password():
    """Set initial customer password. The template for this route contains
    bootstrap.css, bootstrap-theme.css and main.css.

    This is similar to the password reset option with two exceptions:
    it has a longer expiration time and does not require old password.

    :param token: Token generated by
        :meth:`app.models.User.generate_reset_token`

    :return:
    """
    token = request.json['token']
    password = request.json['password']

    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        s.loads(token)
    except BadSignature:
        raise ApiException('Invalid Token', 401)
    try:
        User.set_password(token, password)
    except AttributeError as e:
        raise ApiException(str(e), 400)
    return ApiResponse({'auth': 'authenticated'})

@auth.route('/bosh-session', methods=['GET'])
@login_required
def do_bosh_auth():
    """Start a BOSH session if allowed by configuration

    The following configuration options are required:
    BOSH_ENABLED, BOSH_SERVICE JID, JPASS

    **Example request**:

    .. sourcecode:: http

        GET /auth/bosh-session HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "jid": "do@abusehelper.cert.europa.eu/some-645",
          "rid": 6077172,
          "service": "https://do.cert.europa.eu/bosh",
          "sid": "052352f74b75e6f07b261f8ea86a1e22e5076ef5"
        }


    :resheader Content-Type: this depends on `Accept` header or request

    :>json string service: BOSH service URL
    :>json array rooms: The list of available rooms
    :>json string jid: Jabber ID
    :>json string sid: Session Identifier
    :>json string rid: Request Identifier

    :statuscode 200: BOSH session successfully opened
    """
    if not current_app.config['BOSH_ENABLED']:
        return {}, 503
    c = bosh_client.BOSHClient(
        current_app.config['JID'] + '/' + current_user.email.split('@')[0] +
        '-' + str(random.choice(range(666))),
        current_app.config['JPASS'],
        current_app.config['BOSH_SERVICE']
    )
    if not current_user.can(Permission.ADMINISTER):
        service_url = current_app.config['CP_BOSH_SERVICE']
        rooms = current_app.config['CP_ROOMS']
    else:
        service_url = current_app.config['BOSH_SERVICE']
        rooms = current_app.config['ROOMS']
    return ApiResponse({
        'service': service_url,
        'rooms': rooms,
        'jid': c.jid,
        'sid': c.sid,
        'rid': c.rid,
    })


def do_ldap_authentication(username, password):
    """Authenticate users with CERT-EU LDAP server

    :param username: CERT-EU email or username
    :param password: Account password
    """
    if '@' in username:
        ldap_user = username.split('@')[0]
    else:
        ldap_user = username
    ldap_info, ldap_authenticated = _ldap_authenticate(ldap_user, password)
    if ldap_authenticated:
        u = User.query.filter_by(
            email=ldap_info['userPrincipalName'][0]).first()
        if not u:
            _save_ldap_user(ldap_info)
            u = User.query.filter_by(
                email=ldap_info['userPrincipalName'][0]).first()
        if login_user(u, remember=True):
            return ApiResponse({'auth': 'authenticated'}, 200)

    raise ApiException('Invalid username or password', 401)


def _ldap_authenticate(username, password):
    """Performs a search bind to authenticate a user.

    LDAP server details are defined in :doc:`config`.

    :param username: LDAP username
    :param password: LDAP password
    :return: Returns a tuple of user_info and authentication status
    :rtype: tuple
    """
    user = ldap3_manager.get_user_info_for_username(username)
    ldap_auth = ldap3_manager.authenticate_search_bind(username, password)
    if ldap_auth.status is AuthenticationResponseStatus.success:
        authenticated = True
    else:
        authenticated = False

    return user, authenticated


def _save_ldap_user(ldap_user):
    """Save user information from LDAP to local database

    :param ldap_user: User information as returned by the LDAP server
    """
    u = User(name=ldap_user['name'][0],
             email=ldap_user['userPrincipalName'][0],
             is_admin=True,
             _password='LDAP')
    u.api_key = u.generate_api_key()
    if u.role is None:
        u.role = Role.query.filter_by(permissions=0xff).first()
    db.session.add(u)
    db.session.commit()


def _random_ascii():
    length = random.randint(12, 16)
    return binascii.hexlify(os.urandom(length)).decode('ascii')


@auth.route('/toggle-2fa', methods=['POST'])
@validate('auth', 'toggle_2fa')
@login_required
def toggle_2fa():
    """Toggle Two-Factor authentication

    **Example request**:

    .. sourcecode:: http

        POST /auth/toggle-2fa HTTP/1.1
        Host: do.cert.europa.eu
        Content-Type: application/json

        {
          "otp_toggle": true,
          "totp": 453007
        }

    **Example success response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 31

        {
          "message": "Your options have been saved"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json boolean otp_toggle: Enable or disable second authentication factor
    :<json integer totp: 6 digit TOTP
    :>json string message: Action status

    :statuscode 200: Password successfully changed
    """
    otp_toggle = request.json.get('otp_toggle', False)
    totp = request.json.pop('totp', False)
    user = User.query.filter_by(id=current_user.id).first_or_404()
    if not otp_toggle:
        user.otp_enabled = False
        db.session.add(user)
        db.session.commit()
        return ApiResponse({'message': 'Your options have been saved'})
    if otp_toggle and user.verify_totp(totp):
        user.otp_enabled = True
    else:
        raise ApiException('Authentication code verification failed')
    db.session.add(user)
    db.session.commit()
    return ApiResponse({'message': 'Your options have been saved'})


@auth.route('/2fa-qrcode')
@login_required
def twofactor_qrcode():
    """Return a QRcode of the TOTP URI for the current user"""
    user = User.query.filter_by(id=current_user.id).first_or_404()
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
