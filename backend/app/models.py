import os
import base64
import datetime
import binascii
import hashlib
import random
import csv
import yaml
from urllib.error import HTTPError
import onetimepass
from app import db, login_manager, config
from sqlalchemy import desc, event, text, or_, UniqueConstraint
from sqlalchemy.orm import aliased, deferred
from sqlalchemy.dialects import postgres
from flask_sqlalchemy import BaseQuery
from flask import current_app, request
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from itsdangerous import BadTimeSignature, TimedJSONWebSignatureSerializer
from app.utils.mixins import SerializerMixin
from app.utils.inflect import pluralize
from validate_email import validate_email
from app.utils.mail import send_email
from sqlalchemy.exc import IntegrityError    
import phonenumbers
import time
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import re

import sys
import functools

print = functools.partial(print, flush=True)

# from pprint import pprint

#: we don't have an app context yet,
#: we need to load the configuration from the config module
_config = config.get(os.getenv('DO_CONFIG') or 'default')

def check_phonenumber(phonenumber):
    try:
        if not phonenumber:
            phonenumber = None
        else:
            x = phonenumbers.parse(phonenumber, None)
            phonenumber = re.sub(r'\s+', '', phonenumber)
            m = re.search(r'^\+\d+$', phonenumber)
            if not m:
                raise AttributeError(phonenumber, 'number has to start with a + and may only contain numbers')
    except phonenumbers.phonenumberutil.NumberParseException as err:
        # db.session.rollback()
        raise AttributeError(phonenumber, 'seems not to be a valid phonenumber')
    return phonenumber

def check_password_quality(password):
    import re
    error_text = ''
    ea = []
    if len(password) < 8:
        ea.append('password too short')
    if not re.search(r"\d", password):
        ea.append('password has to contain a number')
    if not re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password):
        ea.append('password has to contain a special character')
    if not re.search(r"[A-Z]", password):
        ea.append('password has to contain an upper case letter')
    if not re.search(r"[a-z]", password):
        ea.append('password has to contain a lower case letter')

    error_text = '; '.join(ea)
    return error_text


emails_organizations = db.Table(
    'emails_organizations', db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column(
        'email_id',
        db.Integer,
        db.ForeignKey('emails.id')
    ),
    db.Column(
        'organization_id',
        db.Integer,
        db.ForeignKey('organizations.id')
    ),
    # db.UniqueConstraint('email_id', 'organization_id', name='eo_idx')
)
tags_vulnerabilities = db.Table(
    'tags_vulnerabilities', db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('tags.id')
    ),
    db.Column(
        'vulnerability_id',
        db.Integer,
        db.ForeignKey('vulnerabilities.id')
    )
)


class FilteredQuery(BaseQuery):
    """
    .. todo:: Remove the deleted field and all logic associated with it.
        Audit log will record any changes
    """
    def get(self, ident):
        # override get() so that the flag is always checked in the
        # DB as opposed to pulling from the identity map. - this is optional.
        return BaseQuery.get(self.populate_existing(), ident)

    def __iter__(self):
        return BaseQuery.__iter__(self.private())

    def from_self(self, *ent):
        # override from_self() to automatically apply
        # the criterion too.   this works with count() and
        # others.
        return BaseQuery.from_self(self.private(), *ent)

    def private(self):
        mzero = self._mapper_zero()
        if mzero is not None:
            crit = mzero.class_.deleted == 0
            return self.enable_assertions(False).filter(crit)
        else:
            return self


class Model(db.Model):
    __abstract__ = True
    __public__ = ()
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    #: Flask-SQLAlchemy's base model class
    #: (which is also SQLAlchemy's declarative base class) defines a
    #: constructor which takes **kwargs and stores all the arguments given,
    #: so it isn't really necessary to define a constructor.
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        # do custom initialization here

    @classmethod
    def fromdict(cls, json):
        items = {}
        for key, val in json.items():
            if isinstance(val, (str, int, list)):
                if hasattr(cls, key):
                    items[key] = val
        return cls(**items)

    def from_json(self, json):
        for attr, value in json.items():
            if isinstance(value, (str, int, list)) or value is None:
                if hasattr(self, attr):
                    setattr(self, attr, value)
        return self

    @classmethod
    def get(cls, ident):
        return cls.query.get(ident)

    def __str__(self):
        return '{} #{}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        kws = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        args_ = []
        for k, v in kws.items():
            args_.append('{!s}={!r}'.format(k, str(v)))
        return '{}({})'.format(self.__class__.__name__, ', '.join(args_))


def get_mailman_client():
    """Return a mailman client instance to be used by the model.

    .. note:: Printing the instance will print the API crendential
    """
    return Client('{0}/{1}'.format(
        current_app.config['MAILMAN_REST_API_URL'],
        current_app.config['MAILMAN_REST_API_VERSION']),
        current_app.config['MAILMAN_REST_API_USER'],
        current_app.config['MAILMAN_REST_API_PASS'])


class MailmanApiError(Exception):
    pass


class MailmanQuery:

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint

    def all(self):
        try:
            return getattr(get_mailman_client(), pluralize(self.endpoint))
        except AttributeError:
            raise MailmanApiError
        except MailmanConnectionError as e:
            raise MailmanApiError(e)

    def get(self, **kwargs):
        try:
            method = getattr(get_mailman_client(), 'get_' + self.endpoint)
            return method(**kwargs)
        except AttributeError as e:
            raise MailmanApiError(e)
        except HTTPError as e:
            raise
        except MailmanConnectionError as e:
            raise MailmanApiError(e)

    def get_or_404(self, **kwargs):
        try:
            return self.get(**kwargs)
        except HTTPError as e:
            raise
        except MailmanConnectionError as mce:
            raise MailmanApiError(mce)


class MailmanModel:

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint

    @classmethod
    def get(cls, **kwargs):
        return cls.query.get(**kwargs)

    @classmethod
    def get_or_404(cls, **kwargs):
        return cls.query.get_or_404(**kwargs)


class MailmanDomain(MailmanModel):

    query = MailmanQuery('domain')


class MailmanList(MailmanModel):

    query = MailmanQuery('list')


class MailmanUser(MailmanModel):

    query = MailmanQuery('user')


class MailmanMember(MailmanModel):

    query = MailmanQuery('member')


class User(UserMixin, Model, SerializerMixin):
    """User model"""
    __tablename__ = 'users'
    __public__ = ('id', 'name', 'otp_enabled', 'picture', 'birthdate', \
                  'title', 'email', 'picture_filename', 'alias_user_id')

    __private__ = ('reset_token', 'reset_token_valid_to', 'api_key', \
                   'otp_enabled', 'origin', 'login_timestamp')

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    alias_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    _name = db.Column('name', db.String(255), nullable=False)
    _password = db.Column('password', db.String(255), nullable=False, default=binascii.hexlify(os.urandom(12)).decode())
    _email = db.Column('email', db.String(255), unique=True)
    api_key = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean(), default=False)
    deleted = db.Column(db.Integer, default=0)
    ts_deleted = db.Column(db.DateTime)
    otp_secret = db.Column(db.String(16))
    otp_enabled = db.Column(db.Boolean, default=False, nullable=False)
    picture = deferred(db.Column(db.Text))
    picture_filename = db.Column(db.String(255))
    birthdate = db.Column(db.Date)
    title = db.Column(db.String(255))
    origin = db.Column(db.String(255))
    _reset_token = db.Column(db.String(255))
    _reset_token_valid_to = db.Column(db.DateTime)
    _login_timestamp = db.Column('login_timestamp', db.DateTime)

    _orgs = []
    _org_ids = []
    _organizations_list = []
    multi_tree_org_id = []
    multi_tree_org_raw = []

    aliased_users = db.relationship('User')

    user_memberships = db.relationship(
        'OrganizationMembership',
        # backref='user_memberships',
        lazy='subquery',
        back_populates="user",
    )

    user_memberships_dyn = db.relationship(
        'OrganizationMembership',
        lazy='dynamic',
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.api_key = self.generate_api_key()
        '''
        if self.email in current_app.config['ADMINS']:
            self.role = Role.query.filter_by(permissions=0xff).first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()
        if self.id is None:
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
        '''

    def get_totp_uri(self):
        return 'otpauth://totp/{0}?secret={1}&issuer=CERT-EU' \
            .format(self.email, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret, window=1)

    @property
    def login_timestamp(self):
        return self._login_timestamp

    @login_timestamp.setter
    def login_timestamp(self, login_timestamp):
        self._login_timestamp = login_timestamp

    @property
    def password(self):
        """User password is a read-only property.

        :raises: :class:`AttributeError`
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        password_errors = check_password_quality(password)
        if password_errors:
            raise AttributeError(password_errors)
        self._password = generate_password_hash(
            password, method='pbkdf2:sha512:100001', salt_length=32
        )    
        # self.reset_password_send_email(self.email)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def email(self):
        if self.alias_user_id:
            parent_user = User.get(self.alias_user_id)
            return parent_user.email
        return self._email

    @email.setter
    def email(self, email):
        email = email.lower()
        if not self.deleted and not validate_email(email):
            raise AttributeError(email, 'seems not to be a valid email address')
        user = User.query.filter_by(_email=email).first()
        if user:
            if self.id != user.id:
                raise ValueError(email, 'duplicate email', user)
        
        """
        see https://github.com/certat/do-portal/issues/112
        send change email if user is orgadmin for at least one org
        """
        if self._email is not None and \
            (self._email != email) and \
            self.get_organization_memberships():

            send_email('Email Change', [email, self._email],
                   'auth/email/change_orgadmin_email', user=self,
                   newemail=email )

        self._email = email

    @property
    def name(self):
        if self.alias_user_id is not None:
            parent_user = User.get(self.alias_user_id)
            return '# alias user # ' + parent_user.name
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def reset_token(self):
        return self._reset_token

    @reset_token.setter
    def reset_token(self, reset_token):
        self._reset_token = reset_token 
        delta = datetime.timedelta(seconds = 900)
        self._reset_token_valid_to = datetime.datetime.today() + delta
        # current_app.logger.debug('user', self.id, reset_token)

    @property
    def reset_token_valid_to(self):
        return self._reset_token_valid_to

    @classmethod
    def authenticate(cls, email, password):
        if not email:
            return None, False
        user = cls.query.filter(cls._email == email).first()
        if user:
            authenticated = user.check_password(password)
            # user has to be 'OrgAdmin' for at least one organisation
            orgs = user.get_organization_memberships()
            if orgs == []:
                authenticated = False
        else:
            authenticated = False
        user.login_timestamp = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return user, authenticated

    @classmethod
    def reset_password_send_email(cls, email):
        user = cls.query.filter(cls._email == email).first()
        if user:
            orgs = user.get_organization_memberships()
            if orgs == []:
                return False
            # password = binascii.hexlify(os.urandom(random.randint(6, 8))).decode('ascii')+'aB1$'
            # user.password = password
            token = user.generate_reset_token()

            send_email('Austrian Energy CERT - Kontaktdatenbank: Account-Aktivierung/Passwort-Reset', [user.email],
                   'auth/email/ec_reset_password', user=user,
                   token=token.decode("utf-8"), email=email )
            db.session.add(user)
            db.session.commit()
            return token
        return False

    def get_auth_token(self, last_totp=None):
        """Think of :class:`URLSafeTimedSerializer` `salt` parameter as
        namespace instead of salt. `The salt explained:
        <https://pythonhosted.org/itsdangerous/#the-salt>`_.
        """
        data = [self.email, self._password, str(self.id)]
        if last_totp:
            data.append(last_totp)
        s = URLSafeTimedSerializer(
            current_app.config['SECRET_KEY'],
            salt='user-auth',
            signer_kwargs=dict(
                key_derivation='hmac',
                digest_method=hashlib.sha256)
        )
        return s.dumps(data)

    def generate_reset_token(self, expiry=900):
        """Generate a JSON Web Signature that will be used to reset customer's
        password. For details see
        :meth:`itsdangerous.JSONWebSignatureSerializer.dumps`

        :param expiry: Token expiration time (seconds)
        :return:
        """
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expiry
        )

        if self.alias_user_id:
            user = User.get(self.alias_user_id) 
        else:
            user = self
       
         
        user.reset_token = s.dumps({'user_id': user.id}).decode("utf-8")
        # add user AND alias user(s) in caller #  db.session.add(user)
        return s.dumps({'user_id': user.id})

    def reset_password(self, token, new_pass):
        """Reset password. Token is generated by
        :meth:`~User.generate_reset_token`

        :param token:
        :param new_pass:
        :return:
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('user_id') == self.id:
            self.password = new_pass
            db.session.add(self)
            db.session.commit()
            return True
        return False

    @classmethod
    def set_password(cls, token, passwd):
        """Set the password for user

        :param token:
        :param passwd:
        :return:
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        data = s.loads(token)
        user = cls.get(data.get('user_id'))
        if user.reset_token is None:
            raise AttributeError('Token already used')
        user.password = passwd
        user.reset_token = None
        user._reset_token_valid_to = None
        
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def create_test_user():
        """Create dummy user for running tests
        """
        if current_app.config['TESTING']:
            name = 'test-{}'.format(User.random_str(8))
            email = 'test-{}@{}.com'.format(
                User.random_str(8), User.random_str(8))
            current_app.config['ADMINS'].append(email)
            Role._Role__insert_defaults()
            user = User(name=name, email=email, password='e9c9525ef737',
                        otp_enabled=True)
            user.api_key = user.generate_api_key()
            db.session.add(user)
            db.session.commit()
            return user

    def create_alias_user(self, organization_id = None):
        user = User(name = '# is alias of ' + str(self.id) , password = 'XX 12 no password set %%',
                    otp_enabled = False, alias_user_id = self.id, deleted = 0)
        db.session.add(user)
        return user

    def generate_api_key(self):
        rand = self.random_str()
        return hashlib.sha256(rand.encode()).hexdigest()

    @staticmethod
    def create(user_dict):
        try:
            user = User.fromdict(user_dict)
            message = 'User added'
        except ValueError as ae:
            existing_user = ae.args[2]
            user = existing_user.create_alias_user()    
            message = 'User aliased'

        db.session.add(user) 
        return(user, message)

    @staticmethod
    def delete_unused_users():
        '''
        select id, name, email, deleted from users where id not in
          (select user_id from organization_memberships om where om.deleted = 0) and
          deleted = 0;
        '''
        subquery = db.session.query(OrganizationMembership.user_id).filter_by(deleted=0)
        unused_users = User.query.filter_by(deleted=0) \
                 .filter(User.id.notin_(subquery))
        for user in unused_users:
            user.mark_as_deleted()
            db.session.add(user)
        return unused_users.count()

    @staticmethod
    def random_str(length=64):
        return binascii.hexlify(os.urandom(length)).decode()


    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    _role_cache = {}
    def get_role_by_name(self, role_name):
        if role_name in self._role_cache:
            return self._role_cache[role_name]
        else:
            role = MembershipRole.query.filter_by(name = role_name).first()
            self._role_cache[role_name] = role
            return role


    def may_handle_user(self, user):
        """checks if the user object it is called on
           (which MUST be an OrgAdmin)
            may manipulate the user of the parameter list
        """
        oms = self.get_organization_memberships()
        for um in user.user_memberships:
           if um.organization_id in self.multi_tree_org_id:
              return True
        return False

    def mark_as_deleted(self):
        self.deleted = 1
        self.ts_deleted = datetime.datetime.utcnow()
        if self.email:
            self.email = str(time.time()) + self.email
        db.session.add(self)
        for um in self.user_memberships:
            um.mark_as_deleted(delete_last_membership = True)

    def may_handle_organization(self, org):
        """checks if the user object it is called on
           (which MUST be an OrgAdmin)
            may manipulate the organization of the parameter list
        """
        self.get_organization_memberships()
        if org.id in self.multi_tree_org_id:
            return True
        return False

    _tree_cache = {};

    '''
    def _org_tree_iterator(self, org_id):
        if org_id in self._tree_cache:
           self._tree_cache[org_id] += 1
        else:
           self._tree_cache[org_id] = 1

        sub_orgs = Organization.query.filter_by(parent_org_id = org_id)
        for sub_org in sub_orgs:
           # print(sub_org.full_name + str(sub_org.id))
           self._orgs.append(sub_org.organization_memberships)
           self._org_ids.append(sub_org.id)
           self._org_tree_iterator(sub_org.id)
    '''

    def _org_tree_raw(self, org_id, limit = 1000, offset = 0):
        results = db.engine.execute(
                text("""with recursive sub_orgs as (
                              select id,
                              abbreviation,
                              full_name,
                              display_name,
                              deleted,
                              parent_org_id,
                              'n/a'::text parent_org_abbreviation,
                              0 depth
                         from organizations
                   where id = :b_parent_org_id
                   union
                   select distinct o.id, o.abbreviation, o.full_name, o.display_name, o.deleted, o.parent_org_id, s.abbreviation::text, s.depth + 1 from organizations o
                   join sub_orgs s ON s.id = o.parent_org_id)
                   select * from sub_orgs where deleted = 0 limit :b_limit offset :b_offset
                """), {'b_parent_org_id': org_id, 'b_limit': limit, 'b_offset': offset});

        self._organizations_list = []

        for r in results.fetchall():
            h = {}
            for i, k in enumerate(results.keys()):
                h[k] = r[i]

            self._organizations_list.append(h)
        return self._organizations_list

    def _org_tree(self, org_id, limit = 1000, offset = 0):
        results = db.engine.execute(
                text("""with recursive sub_orgs as (select id, abbreviation, full_name, display_name, deleted, parent_org_id, 'n/a'::text, 0 depth from organizations
                   where id = :b_parent_org_id
                   union
                   select o.id, o.abbreviation, o.full_name, o.display_name, o.deleted, o.parent_org_id, s.abbreviation::text, s.depth + 1 from organizations o
                   join sub_orgs s ON s.id = o.parent_org_id)
                   select * from sub_orgs limit :b_limit offset :b_offset
                """), {'b_parent_org_id': org_id, 'b_limit': limit, 'b_offset': offset});

        self._org_ids = []
        for row in results:
            self._org_ids.append(row[0])
        return self._org_ids
 

    def get_organization_memberships(self):
        """ returns a list of OrganizationMembership records"""
        """ self MUST be a logged in admin, we find all nodes (and subnodes)
            where the user is admin an return ALL memeberships of those nodes
            in the org tree """
        admin_role = self.get_role_by_name('OrgAdmin')
        
        stmt_user_ids = db.session.query(User.id). \
            filter(or_(User.id == self.id, User.alias_user_id == self.id)).subquery()
        orgs_admins = OrganizationMembership.query. \
            filter(OrganizationMembership.user_id.in_(stmt_user_ids)). \
            filter_by(membership_role_id = admin_role.id, deleted = 0).all()

        if (not orgs_admins):
           return []

        self._orgs = [orgs_admins]
        self._org_ids = [org.organization.id for org in orgs_admins]

        # find all orgs where the org.id is the parent_org_id recursivly
        #  for org in orgs_admin:
        
        self.multi_tree_org_id = []  
        self.multi_tree_org_raw = []  
        for oa in orgs_admins:
           # self._org_tree_iterator(oa.organization_id)
           self.multi_tree_org_id.extend(self._org_tree(oa.organization_id))
           self.multi_tree_org_raw.extend(self._org_tree_raw(oa.organization_id))

        oms = OrganizationMembership.query.filter( \
                     OrganizationMembership.organization_id.in_(self.multi_tree_org_id)) \
                     .filter(OrganizationMembership.deleted == 0)
        return oms

    def get_organizations(self, limit = 1000, offset = 0):
        """returns a list of Organization records"""
        oms = self.get_organization_memberships()
        if not self._org_ids:
            return []
        return Organization.query.filter(Organization.id.in_(self.multi_tree_org_id)) \
                    .limit(limit).offset(offset)

    def get_organizations_raw(self, limit = 5, offset = 0):
        """returns a list of Organization records"""
        oms = self.get_organization_memberships()
        if not self._org_ids:
            return []
        return self.multi_tree_org_raw

    def get_users(self):
        """returns a list of unique User records"""
        oms = self.get_organization_memberships()
        # for om in oms:
        users = []
        ud = {}
        for om in oms:
            if om.user.id not in ud:
                if om.user.deleted != 1:
                    users.append(om.user)                
                ud[om.user.id] = 1

        return users

    def get_memberships(self, membership_id = None):
        """returns all memeberships for user"""
        if membership_id:
            return self.user_memberships_dyn.filter_by(id = membership_id, deleted = 0).first()
        else:
            return self.user_memberships_dyn.filter_by(deleted = 0)

    def is_authenticated(self):
        print(self.name)

class Permission:
    """Permissions pseudo-model. Uses 8 bits to assign permissions.
    Each permission is assigned a bit possion and for each role the
    permissions that are allowed will have their bits set to 1.

    When granularity is needed use roles and permissions.
    For simple cases (users & admins) using :attr:`User.is_admin` is enough.

    Permissions:

    +---------------+-----------------+---------------------------------------+
    | Permission    | Bit (Hex)       | Description                           |
    +===============+=================+=======================================+
    | ORGADMIN      | 00000001 (0x01) | Allow editing organization details    |
    +---------------+-----------------+---------------------------------------+
    | SUBMITSAMPLE  | 00000010 (0x02) | User can submit malware samples       |
    +---------------+-----------------+---------------------------------------+
    | ADDCPACCOUNT  | 00000100 (0x04) | User can register contact emails for  |
    |               |                 | CP access.                            |
    +---------------+-----------------+---------------------------------------+
    | SLAACTIONS    | 00001000 (0x08) | User is part of an organization that  |
    |               |                 | has signed an SLA with CERT-EU.       |
    +---------------+-----------------+---------------------------------------+
    | ADMINISTER    | 10000000 (0x80) | Administrative access                 |
    +---------------+-----------------+---------------------------------------+

    Roles:

    +---------------+-----------------+---------------------------------------+
    | Role          | Bit (Hex)       | Description                           |
    +===============+=================+=======================================+
    | Anonymous     | 00000000 (0x00) | No access                             |
    +---------------+-----------------+---------------------------------------+
    | Constituent   | 00000111 (0x07) | Constituents can edit their details,  |
    |               |                 | submit malware samples and register   |
    |               |                 | other contact emails for CP access.   |
    +---------------+-----------------+---------------------------------------+
    | SLA           | 00001111 (0x0f) | All Constituent role permissions plus |
    | Constituent   |                 | SLAACCOUNT.                           |
    +---------------+-----------------+---------------------------------------+
    | Administrator | 11111111 (0x80) | Administrator rights (Full access)    |
    +---------------+-----------------+---------------------------------------+

    >>> '0x{0:02x}'.format(int('00000100', 2))
    >>> 0x04
    """
    ORGADMIN = 0x01
    SUBMITSAMPLE = 0x02
    ADDCPACCOUNT = 0x04
    SLAACTIONS = 0x08
    ADMINISTER = 0x80


class Role(Model, SerializerMixin):
    __tablename__ = 'roles'
    __public__ = ('id', 'name')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #: True for one role, False for all others
    #: Used as marker when creating new users
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref=db.backref('role'), lazy='dynamic')

    @staticmethod
    def __insert_defaults():
        roles = {
            'Constituent': (Permission.ORGADMIN |
                            Permission.SUBMITSAMPLE |
                            Permission.ADDCPACCOUNT, True),
            'SLA Constituent': (Permission.ORGADMIN |
                                Permission.SUBMITSAMPLE |
                                Permission.ADDCPACCOUNT |
                                Permission.SLAACTIONS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Asn(Model, SerializerMixin):
    __tablename__ = 'asn'
    __public__ = ('id', 'asn', 'as_name')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    asn = db.Column(db.Integer)
    as_name = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Integer, default=0)


class IpRange(Model, SerializerMixin):
    """Classless Inter-Domain Routing"""
    __tablename__ = 'ip_ranges'
    __public__ = ('id', 'ip_range')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    ip_range = db.Column(db.String(255))
    deleted = db.Column(db.Integer, default=0)


class FodyOrg_X_Organization(Model, SerializerMixin):
    __tablename__ = 'fodyorg_x_organization'
    __public__ = ('id', 'organization_id', 'ripe_org_hdl', 'notification_settings')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    # "soft" foreign key
    _ripe_org_hdl = db.Column('ripe_org_hdl', db.String(255), unique=True)
    deleted = db.Column(db.Integer, default=0)
    '''
    _notification_settings = db.relationship('NotificationSetting',
          primaryjoin = "and_(foreign(NotificationSetting.organization_id) == \
                           FodyOrg_X_Organization.organization_id,"
                        "foreign(NotificationSetting.ripe_org_hdl) == \
                          FodyOrg_X_Organization._ripe_org_hdl)")
    '''
    fody_org = None
    _notification_settings = None

    @property
    def ripe_org_hdl(self):
        return self._ripe_org_hdl


    # do not check for an error here, see
    # https://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    # you have to handle it in the caller
    @ripe_org_hdl.setter
    def ripe_org_hdl(self, ripe_org_hdl):
        self.fody_org = FodyOrganization(ripe_org_hdl = ripe_org_hdl)
        self._ripe_org_hdl = self.fody_org.ripe_org_hdl

    @property
    def notification_settings(self):
    #    return self._notification_settings

        nss = NotificationSetting.query \
                .filter_by(ripe_org_hdl=self.ripe_org_hdl,
                           organization_id=self.organization_id ).all()

        notification_settings = {}
        self.fody_org = FodyOrganization(ripe_org_hdl = self.ripe_org_hdl)

        ns_dict = {}
        for ns in nss:
            key = ns.asn if ns.asn else ns.cidr
            ns_dict[key] = \
                  {'delivery_protocol':     ns.delivery_protocol,
                   'delivery_format':       ns.delivery_format,
                   'notification_interval': ns.notification_interval}

        def get_ns_dict(k):
            if k in ns_dict:
                return ns_dict[k]
            else:
                return {}

        notification_settings['asns'] = [{'asn': k,  'notification_setting': get_ns_dict(k)}  for k in self.fody_org.asns]
        notification_settings['cidrs'] = [{'cidr': k, 'notification_setting': get_ns_dict(k)}  for k in self.fody_org.cidrs]
        notification_settings['abusecs'] = self.fody_org.abusecs
        notification_settings['name'] = self.fody_org.name
        self._notification_settings = notification_settings
        return self._notification_settings

    def upsert_notification_setting(self,
                               asn = None,
                               cidr = None,
                               notification_setting = {},
                               delivery_protocol = 'Mail',
                               delivery_format = 'CSV',
                               notification_interval = 604800):


         self.fody_org = FodyOrganization(ripe_org_hdl = self.ripe_org_hdl)
         if not (asn or cidr):
             raise AttributeError('either cidr or asn has to be set')

         if asn and asn not in self.fody_org.asns:
             raise AttributeError('no such asn or not owned', asn, self.fody_org.asns)

         if cidr and cidr not in self.fody_org.cidrs:
             raise AttributeError('no such cidr or not owned', cidr)

         try:
             ns = NotificationSetting.query \
                    .filter_by(asn=asn, cidr=cidr,
                               organization_id=self.organization_id,
                               ripe_org_hdl=self.ripe_org_hdl) \
                    .one()
         except NoResultFound:
             ns = NotificationSetting()
             ns.asn = asn
             ns.cidr = cidr
             ns.organization_id = self.organization_id
             ns.ripe_org_hdl = self.ripe_org_hdl

         ns.delivery_protocol = notification_setting['delivery_protocol'] if 'delivery_protocol' in notification_setting else delivery_protocol
         ns.delivery_format = notification_setting['delivery_format'] if 'delivery_format'  in notification_setting else delivery_format
         ns.notification_interval = notification_setting['notification_interval'] if 'notification_interval'  in notification_setting else notification_interval
         db.session.add(ns)
         self._notification_settings



class NotificationSetting(Model, SerializerMixin):
    __tablename__ = 'notification_settings'
    __public__ = ('delivery_protocol', 'delivery_format', 'notification_interval',
                  'asn', 'cidr', 'ripe_org_hdl', 'organization_id', )

    query_class = FilteredQuery

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    delivery_protocol = db.Column(db.Enum('Mail', 'REST API', 'AMQP', name='delivery_protocol_enum'), default='Mail')
    delivery_format = db.Column(db.Enum('CSV', 'JSON', name='delivery_format_enum'), default='CSV')
    notification_interval = db.Column(db.Integer, default=0)
    ripe_org_hdl = db.Column('ripe_org_hdl', db.String(255))
    asn = db.Column('asn', db.String(255), unique=True)
    cidr = db.Column(postgres.CIDR)
    deleted = db.Column(db.Integer, default=0)

    organization = db.relationship('Organization')

    # ripe_org_hdl = db.Column(db.Integer,
    #               db.ForeignKey('fody.organisation_automatic.ripe_org_hdl'))


    @staticmethod
    def contact_for_netblock(cidr):
        abusecs = []
        default_notification_setting = {
            'delivery_protocol': 'Mail',
            'delivery_format': 'CSV',
            'notification_interval': 604800,
            'cidr': cidr,
            'organization_id': None,
            'ripe_org_hdl': None,
        }

        ripe_org_hdl = FodyOrganization.handle_for_cidr(cidr)
        # check if the ripe handle is associated with an org and excactly this cidr
        ns = NotificationSetting.query. \
             filter_by(ripe_org_hdl=ripe_org_hdl, cidr=cidr).first()

        # no explicit settings for cidr, check if cidr is associated with an organization via ripe handle
        if ns:
            nss = ns.serialize()
        else:
            nss = default_notification_setting
            ns = NotificationSetting.query. \
                filter_by(ripe_org_hdl=ripe_org_hdl).first()
            if ns:
                nss['organization_id'] = ns.organization_id
                nss['ripe_org_hdl'] = ns.ripe_org_hdl

        org_abusecs = []
        if ns:
        # we have a cidr with settings get the local abusecs (if defined)
            org_abusecs = ns.organization.organization_memberships. \
                      filter_by(membership_role = MembershipRole.query.filter_by(name='abuse-c').\
                      one()).all()

        # if cidr is not found in database AttributeError: ('no such cidr', ..) is raised and not caught here
        if org_abusecs:
            abusecs = [o.email for o in org_abusecs]
        else:
            fody_org = FodyOrganization(ripe_org_hdl = ripe_org_hdl)
            abusecs = fody_org.abusecs

        return {'abusecs': abusecs, 'notification_setting': nss }

class FodyOrganization():
    # __tablename__ = 'fody.organisation_automatic'
    __public__ = ('ripe_org_hdl',
                  'name',
                  'organisation_automatic_id',
                  'cidrs',
                  'asns',
                  'abusecs'
                  )

    cidrs   = None
    asns    = None
    abusecs = None

    @staticmethod
    def handle_for_cidr(cidr):
        results = db.engine.execute(
            text("""
            select ripe_org_hdl
                   from fody.organisation_automatic oa
                   join fody.organisation_to_network_automatic o2na
                     on oa.organisation_automatic_id =
                        o2na.organisation_automatic_id
                   join fody.network_automatic na
                     on o2na.network_automatic_id = na.network_automatic_id
                      where address >>= :b_address
            """
            ), {'b_address': cidr})

        for row in results:
            return row[0]
        raise AttributeError('no such cidr', cidr)

    def __init__(self, ripe_org_hdl):
        results = db.engine.execute(
            text("""
            select ripe_org_hdl,
                   name,
                   organisation_automatic_id
              from fody.organisation_automatic
             where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': ripe_org_hdl})

        for row in results:
            self.ripe_org_hdl = row[0]
            self.name = row[1]
            self.organisation_automatic_id = row[2]
            c = self._cidrs
            a = self._asns
            ac = self._abusecs
            return None

        raise AttributeError('no such handle', ripe_org_hdl)

    @property
    def _cidrs(self):
        if self.cidrs:
            return self.cidrs
        results = db.engine.execute(
            text("""
            select address
                   from fody.organisation_automatic oa
                   join fody.organisation_to_network_automatic o2na
                     on oa.organisation_automatic_id =
                        o2na.organisation_automatic_id
                   join fody.network_automatic na
                     on o2na.network_automatic_id = na.network_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.cidrs = [row[0] for row in results]
        return self.cidrs;

    @property
    def _asns(self):
        if self.asns:
            return self.asns
        results = db.engine.execute(
            text("""
            select asn
                   from fody.organisation_automatic oa
                   join fody.organisation_to_asn_automatic o2aa
                     on oa.organisation_automatic_id =
                        o2aa.organisation_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.asns = [str(row[0]) for row in results]
        return self.asns;

    @property
    def _abusecs(self):
        if self.abusecs:
            return self.abusecs
        results = db.engine.execute(
            text("""
            select email
                   from fody.organisation_automatic oa
                   join fody.contact_automatic ca
                     on oa.organisation_automatic_id =
                        ca.organisation_automatic_id
                      where ripe_org_hdl = :b_ripe_org_hdl
            """
            ), {'b_ripe_org_hdl': self.ripe_org_hdl})

        self.abusecs = [str(row[0]) for row in results]


class ContactEmail(Model, SerializerMixin):
    """ContactEmail Association Object
    http://docs.sqlalchemy.org/en/rel_1_0/orm/basic_relationships.html#
    association-object
    http://docs.sqlalchemy.org/en/rel_1_0/orm/extensions/associationproxy.html#
    simplifying-association-objects
    """
    __tablename__ = 'contactemails_organizations'
    __public__ = ('email', 'cp', 'fmb')
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email_id = db.Column(
        db.Integer,
        db.ForeignKey('emails.id'),
        primary_key=True)
    organization_id = db.Column(
        db.Integer,
        db.ForeignKey('organizations.id'),
        primary_key=True
    )
    #: Mark customer portal access for this email
    cp = db.Column('cp_access', db.Boolean(), default=False, doc='CP access')
    #: Functional mailbox marker
    fmb = db.Column(db.Boolean(), default=False, doc='Functional mailbox')
    organization = db.relationship(
        'Organization',
        backref=db.backref(
            'contact_emails',
            lazy='joined',
            cascade='all, delete-orphan'
        )
    )
    email_ = db.relationship('Email')
    email = association_proxy(
        'email_',
        'email',
        creator=lambda eml: Email(email=eml)
    )

    def __repr__(self):
        return '<AssociationProxy Email({0})>'.format(self.email)


class Email(Model, SerializerMixin):
    __tablename__ = 'emails'
    __public__ = ('id', 'email')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    deleted = db.Column(db.Integer, default=0)


class Fqdn(Model, SerializerMixin):
    __tablename__ = 'fqdns'
    __public__ = ('id', 'fqdn', 'typosquats')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    fqdn = db.Column(db.String(255))
    deleted = db.Column(db.Integer, default=0)

    typosquats = db.relationship('Typosquat', lazy='dynamic')


class Typosquat(Model, SerializerMixin):
    __tablename__ = 'fqdns_typosquats'
    __public__ = ('id', 'fqdn', 'dns_a', 'dns_ns', 'dns_mx', 'updated')
    id = db.Column(db.Integer, primary_key=True)
    fqdn_id = db.Column(db.Integer, db.ForeignKey('fqdns.id'))
    fqdn = db.Column(db.String(255))
    dns_a = db.Column(db.String(255), nullable=True)
    dns_ns = db.Column(db.String(255), nullable=True)
    dns_mx = db.Column(db.String(255), nullable=True)
    raw = db.Column(db.Text)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.fqdn)

    def __str__(self):
        return self.fqdn


class OrganizationGroup(Model, SerializerMixin):
    __tablename__ = 'organization_groups'
    __public__ = ('id', 'name', 'color')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    color = db.Column(db.String(7))
    deleted = db.Column(db.Integer, default=0)

    __mapper_args__ = {
        'order_by': desc(id)
    }

    @staticmethod
    def __insert_defaults():
        """Insert sample organization groups"""
        groups = [{'name': 'Constituents', 'color': '#0033CC'},
                  {'name': 'National CERTs', 'color': '#AF2018'},
                  {'name': 'Partners', 'color': '#00FF00'}]
        for group in groups:
            g = OrganizationGroup(**group)
            db.session.add(g)
        db.session.commit()


class Organization(Model, SerializerMixin):
    """

    .. note::

        AssociationProxy on Many-to-Many will not automagically update
        relantionship model. It needs to be updated manually.

    http://docs.sqlalchemy.org/en/latest/faq/ormconfiguration.html?highlight=
    primaryjoin#i-m-using-declarative-and-setting-primaryjoin-secondaryjoin-
    using-an-and-or-or-and-i-am-getting-an-error-message-about-foreign-keys
    """
    __tablename__ = 'organizations'
    __public__ = ('id', 'abbreviation', 'full_name', 'abuse_emails',
                  'ip_ranges', 'fqdns', 'asns', 'old_ID', 'is_sla',
                  'mail_template', 'mail_times', 'group_id', 'group',
                  'contact_emails', 'display_name', 'parent_org_id',
                  'parent_org_abbreviation', 'ripe_handles')
                  # 'notification_settings')

    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(
        'organization_group_id',
        db.Integer,
        db.ForeignKey('organization_groups.id', name='fk_org_group_id')
    )
    is_sla = db.Column(db.Boolean, default=True)
    abbreviation = db.Column(db.String(255), index=True)
    # this is the ID field from AH wiki
    # ("{0:02d}".format(9)
    # we are keeping it for compatibility with the Excel sheets
    old_ID = db.Column(db.String(5))
    full_name = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    mail_template = db.Column(db.String(50), default='EnglishReport')
    # send emails this many seconds apart
    mail_times = db.Column(db.Integer, default=3600)
    ts_deleted = db.Column(db.DateTime)
    deleted = db.Column(db.Integer, default=0)
    # def __init__(self):
    #     self.__parent_org_abbreviation = None

    # too slow ...
    _org_cache = {}

    @hybrid_property
    def parent_org_abbreviation(self):
        if self.parent_org_id:
            if self.parent_org_id in self._org_cache:
                return self._org_cache[self.parent_org_id]['abbreviation']
            else:
                abbr = Organization.query.get(self.parent_org_id).abbreviation
                if not self.parent_org_id in self._org_cache:
                    self._org_cache[self.parent_org_id] = {}
                self._org_cache[self.parent_org_id]['abbreviation'] = abbr
                return abbr
        else:
            return None

    '''
    @hybrid_property
    def parent_org_abbreviation(self):
        return self.__parent_org_abbreviation

    @parent_org_abbreviation.setter
    def parent_org_abbreviation(self, value):
        self.__parent_org_abbreviation = value
    '''

    @property
    def ripe_handles(self):
        return [ro.ripe_org_hdl for ro in self.ripe_organizations]


    @property
    def notification_settings(self):
        return [ro.notification_settings for ro in self.ripe_organizations]

    parent_org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    child_organizations = db.relationship(
        'Organization',
        uselist=True,
        primaryjoin="and_(foreign(Organization.id) == remote(Organization.parent_org_id), "
                    "remote(Organization.deleted) == 0)",
        )

    parent_org = db.relationship('Organization', remote_side=[id])
    child_orgs = db.relationship('Organization',
            # backref=db.backref('parent', remote_side=[id])
            lazy="joined",
            join_depth=5
            )

    organization_memberships = db.relationship(
        'OrganizationMembership',
        backref='orgs_for_user',
        lazy="dynamic"
    )

    group = db.relationship(
        'OrganizationGroup',
        uselist=False,
        foreign_keys=[group_id]
    )
    ip_ranges_ = db.relationship(
        'IpRange',
        lazy='joined',
        cascade='all, delete-orphan',
        primaryjoin="and_(IpRange.organization_id == Organization.id, "
                    "IpRange.deleted == 0)",
    )
    ip_ranges = association_proxy(
        'ip_ranges_',
        'ip_range',
        creator=lambda r: IpRange(ip_range=r)
    )
    abuse_emails_ = db.relationship(
        "Email", secondary=lambda: emails_organizations,
        lazy='joined',
        secondaryjoin=db.and_(
            Email.id == emails_organizations.c.email_id,
            Email.deleted == 0)
    )
    #: Abuse e-mails are read by machines
    abuse_emails = association_proxy(
        'abuse_emails_',
        'email',
        creator=lambda eml: Email(email=eml)
    )

    #: Contact e-mails are used by humans
    contact_emails = association_proxy('contact_emails', 'email')

    asns_ = db.relationship(
        'Asn',
        lazy='joined',
        cascade='all, delete-orphan',
        primaryjoin="and_(Asn.organization_id == Organization.id,"
                    "Asn.deleted == 0)"
    )
    asns = association_proxy(
        'asns_',
        'asn',
        creator=lambda asn: Asn(asn=asn)
    )
    fqdns_ = db.relationship('Fqdn',
        lazy='joined',
        cascade='all, delete-orphan')

    fqdns = association_proxy(
        'fqdns_',
        'fqdn',
        creator=lambda fqdn: Fqdn(fqdn=fqdn)
    )

    users = db.relationship(
        'User', backref=db.backref('organizations'), lazy='dynamic')

    __mapper_args__ = {
        'order_by': abbreviation
    }

    ripe_organizations = db.relationship(
        'FodyOrg_X_Organization',
        backref='fody_orgs_for_organization'
    )

    notification_settings = db.relationship(
        'NotificationSetting',
        backref='notification_settings_for_organization'
    )

    @ripe_handles.setter
    def ripe_handles(self, ripe_handles):
        current_ripe_handles = [ro.ripe_org_hdl for ro in self.ripe_organizations]
        for ripe_handle in ripe_handles:
            if ripe_handle in current_ripe_handles:
                current_ripe_handles.remove(ripe_handle)
            else:
                forg_x_org = FodyOrg_X_Organization();
                forg_x_org.ripe_org_hdl = ripe_handle
                self.ripe_organizations.append(forg_x_org)

        for ripe_handle in current_ripe_handles:
            forg_x_org = FodyOrg_X_Organization.query   \
                .filter_by(_ripe_org_hdl = ripe_handle) \
                .filter_by(organization_id = self.id).one()
            # forg_x_org.delete();
            self.ripe_organizations.remove(forg_x_org)
            db.session.delete(forg_x_org)



    @staticmethod
    def from_collab(customer):
        """Import organization from collab

        :param customer: ``CollabCustomer``
        :return:
        :rtype:
        """
        org = Organization(abbreviation=customer.name)
        conf = customer.config
        try:
            org.full_name = conf['Full name'][0]
        except IndexError:
            current_app.log.error(
                'Organization {} is missing full name...'.format(customer[0])
            )
        try:
            org.mail_times = conf['Mail times'][0]
        except IndexError:
            current_app.log.debug('Using default mail times...')
        try:
            org.mail_template = conf['Mail template'][0]
        except IndexError:
            current_app.log.debug('Using default template...')
        try:
            org.old_ID = conf['ID'][0]
        except IndexError:
            current_app.log.debug('Missing ID...')

        _props_map = {
            'ip_ranges': 'IP range',
            'fqdns': 'FQDN',
            'asns': 'ASN',
            'abuse_emails': 'Abuse email',
            'contact_emails': 'Point of Contact'
        }

        for key, collab_key in _props_map.items():
            if key == 'contact_emails':
                for eml in conf[collab_key]:
                    org.contact_emails.append(
                        ContactEmail(email_=Email(email=eml), cp=0))
            else:
                setattr(org, key, conf[collab_key])

        org.group_id = 1
        return org

    # organization.mark_as_deleted
    def mark_as_deleted(self):
        if self.child_organizations:
            raise AttributeError('Organisation cannot be deleted because it has child organisations')
        self.deleted = 1
        self.ts_deleted = datetime.datetime.utcnow()
        for um in self.organization_memberships:
            um.mark_as_deleted(delete_last_membership = True)

    # STUB
    def has_child_organizations(self):
        return True

    # STUB
    def can_be_deleted(self):
        # not has_child_organizations and not has associated OrganizationMembership
        # records
        return True

    def __repr__(self):
        return '{} #{}'.format(self.__class__.__name__, self.abbreviation)


class Tag(Model, SerializerMixin):
    __tablename__ = 'tags'
    __public__ = ('id', 'name')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Vulnerability(Model, SerializerMixin):
    __tablename__ = 'vulnerabilities'
    __public__ = ('id', 'constituent', 'do', 'check_string', 'types',
                  'updated', 'url', 'reported', 'patched', 'request_method',
                  'tested', 'request_data', 'request_response_code',
                  'incident_id', 'reporter_name', 'reporter_email',
                  'organization_id', 'notes', 'published', 'scanable',
                  'test_type')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    incident_id = db.Column(db.Integer, nullable=True)
    reporter_name = db.Column(db.String(255))
    reporter_email = db.Column(db.String(255))
    #: PoC
    url = db.Column(db.Text)
    request_method = db.Column(db.Enum('GET', 'POST', 'PUT', name='httpverb'), default='GET')
    request_data = db.Column(db.Text)
    check_string = db.Column(db.Text)
    test_type = db.Column(db.Enum('request', name='test_type_enum'), default='request')
    request_response_code = db.Column(db.Integer, nullable=True)
    tested = db.Column(db.DateTime, nullable=True)
    reported = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    patched = db.Column(db.DateTime, nullable=True)
    #: Publish in the Hall of Fame
    published = db.Column(db.Boolean, default=False)
    scanable = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    deleted = db.Column(db.Integer, default=0)

    organization_ = db.relationship('Organization')
    constituent = association_proxy('organization_', 'abbreviation')

    user = db.relationship('User')
    do = association_proxy('user', 'name')

    labels_ = db.relationship(
        'Tag', secondary=tags_vulnerabilities,
        backref=db.backref('vulnerabilities'))
    types = association_proxy(
        'labels_',
        'name',
        creator=lambda l: Tag(name=l)
    )
    __mapper_args__ = {
        'order_by': desc(id)
    }


class Deliverable(Model, SerializerMixin):
    """Sample deliverables: CIMBL, CITAR, etc.
    """
    __tablename__ = 'deliverables'
    __public__ = ('id', 'name')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    deleted = db.Column(db.Integer, default=0)


class DeliverableFile(Model, SerializerMixin):
    """The files that we upload
    """
    __tablename__ = 'deliverable_files'
    __public__ = ('id', 'name', 'created', 'type')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    deliverable_id = db.Column(db.Integer, db.ForeignKey('deliverables.id'))
    name = db.Column(db.String(255), nullable=False)
    #: File will be available to SLA constituents only
    is_sla = db.Column(db.Boolean, default=0)
    deleted = db.Column(db.Integer, default=0)

    deliverable_ = db.relationship(
        'Deliverable', uselist=False,
        foreign_keys=[deliverable_id],
        backref=db.backref('files')
    )
    type = association_proxy(
        'deliverable_',
        'name'
    )

    __mapper_args__ = {
        'order_by': desc(id)
    }


class Task(Model):
    __tablename__ = 'tasks_taskmeta'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255), nullable=True, unique=True)
    status = db.Column(db.String(50), nullable=True)
    result = db.Column(db.LargeBinary, nullable=True)
    date_done = db.Column(db.DateTime, nullable=True)
    traceback = db.Column(db.Text, nullable=True)


class TaskGroup(Model):
    __tablename__ = 'tasks_groupmeta'
    id = db.Column(db.Integer, primary_key=True)
    taskset_id = db.Column(db.String(255), nullable=True, unique=True)
    result = db.Column(db.LargeBinary, nullable=True)
    date_done = db.Column(db.DateTime, nullable=True)


class AHBotType(Model, SerializerMixin):
    __tablename__ = 'ah_bot_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class AHBot(Model, SerializerMixin):
    """Model for AbuseHelper bots.
    """
    __tablename__ = 'ah_bots'
    __public__ = ('id', 'name')
    id = db.Column(db.Integer, primary_key=True)
    bot_type_id = db.Column(
        db.Integer,
        db.ForeignKey('ah_bot_types.id'))
    name = db.Column(db.String(30))
    description = db.Column(db.String(255))

    type = db.relationship(
        'AHBotType', uselist=False,
        foreign_keys=[bot_type_id]
    )


class AHStartupConfig(Model, SerializerMixin):
    __tablename__ = 'ah_startup_configs'
    # belongsTo AbuseHelperBot
    # hasMany AbuseHelperStartupParam
    # HABTM AbuseHelperStartupTemplate
    id = db.Column(db.Integer, primary_key=True)
    ah_bot_id = db.Column(
        db.Integer,
        db.ForeignKey('ah_bots.id'))
    enabled = db.Column(db.Boolean(), default=False)
    #: python module or PATH
    module = db.Column(db.String(255))
    state = db.Column(db.Boolean(), default=False, nullable=True)
    pid = db.Column(db.Integer, nullable=True)
    started = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    stopped = db.Column(db.DateTime, nullable=True,
                        onupdate=datetime.datetime.utcnow)
    ah_bot = db.relationship(
        'AHBot',
        foreign_keys=[ah_bot_id]
    )


class AHStartupConfigParam(Model, SerializerMixin):
    __tablename__ = 'ah_startup_config_params'
    # belongsTo AbuseHelperStartupConfig
    id = db.Column(db.Integer, primary_key=True)
    ah_startup_config_id = db.Column(
        db.Integer,
        db.ForeignKey('ah_startup_configs.id'))
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    ah_startup_config = db.relationship(
        'AHStartupConfig',
        foreign_keys=[ah_startup_config_id],
        backref=db.backref('params')
    )


class AHRuntimeConfig(Model, SerializerMixin):
    __tablename__ = 'ah_runtime_configs'
    # belongsTo AbuseHelperBot
    # hasMany AbuseHelperRuntimeConfigParam
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(2))
    ah_bot_id = db.Column(
        db.Integer,
        db.ForeignKey('ah_bots.id'))
    ah_bot = db.relationship(
        'AHBot',
        foreign_keys=[ah_bot_id]
    )


class AHRuntimeConfigParam(Model, SerializerMixin):
    __tablename__ = 'ah_runtime_config_params'
    # belongsTo AbuseHelperRuntimeConfig
    id = db.Column(db.Integer, primary_key=True)
    ah_runtime_config_id = db.Column(
        db.Integer,
        db.ForeignKey('ah_runtime_configs.id'))
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    ah_runtime_config = db.relationship(
        'AHRuntimeConfig',
        foreign_keys=[ah_runtime_config_id],
        backref=db.backref('params')
    )


class Sample(Model, SerializerMixin):
    """Model for samples that will be submitted for analysis
    """
    __tablename__ = 'samples'
    __public__ = ('id', 'created', 'filename', 'md5', 'sha1', 'sha256',
                  'sha512', 'ctph')
    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', name='fk_sample_user_id'))
    #: For archives. All files within an archive will have the parent_id set
    #: to the archive unique ID
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('samples.id'),
        nullable=True)
    #: Submitted filename
    filename = db.Column(db.Text, nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    sha1 = db.Column(db.String(40), nullable=False)
    #: SHA-256 sum of file contents
    sha256 = db.Column(db.String(64), nullable=False)
    sha512 = db.Column(db.String(128), nullable=False)
    #: Context triggered piecewise hash
    ctph = db.Column(
        db.Text, nullable=False,
        doc='Context triggered piecewise hash')
    infected = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Integer, default=0)

    __mapper_args__ = {'order_by': desc(id)}

    reports = db.relationship('Report')
    user = db.relationship(
        'User', uselist=False,
        foreign_keys=[user_id],
        backref=db.backref('samples')
    )
    parent = db.relationship(
        'Sample', backref=db.backref('children'),
        remote_side=[id]
    )


class ReportType(Model, SerializerMixin):
    __tablename__ = 'report_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    @staticmethod
    def __insert_defaults():
        types = ['Static analysis', 'AntiVirus scan', 'Dynamic analysis']
        for type_ in types:
            r = ReportType(name=type_)
            db.session.add(r)
        db.session.commit()


class Report(Model, SerializerMixin):
    __tablename__ = 'reports'
    __public__ = ('id', 'created', 'type', 'report')
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('report_types.id'))
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    report = db.Column(db.Text)

    __mapper_args__ = {'order_by': desc(id)}

    type_ = db.relationship('ReportType')
    type = association_proxy(
        'type_',
        'name'
    )


class Contact(Model):
    """Not used"""
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    deleted = db.Column(db.Integer, default=0)

class Country(Model, SerializerMixin):
    __tablename__ = 'countries'
    __public__ = ('id', 'cc', 'name')
    query_class = FilteredQuery
    cc = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Integer, default=0)
    users_for_country = db.relationship(
        'OrganizationMembership',
        back_populates='country'
    )

    @staticmethod
    def __insert_defaults():
##        countries = [
##          ['AT',               'Austria'],
##          ['DE',               'Germany'],
##          ['CH',               'Switzerland'],
##        ]
##        for r in countries:
##            country = Country.query.filter_by(name=r[0]).first()
##
##            if country is None:
##                country = Country(cc=r[0], name=r[1] )
##                db.session.add(country)
##        db.session.commit()
        with open('install/iso_3166_2_countries.csv') as csvfile:
            data = csv.reader(csvfile, delimiter = ',')
            data = list(data)
            for r in data[2:]:
            #    print(r[1], r[10])
                country = Country.query.filter_by(cc=r[10]).first()
                if country is None:
                    country = Country(cc=r[10], name=r[1] )
                    db.session.add(country)
            db.session.commit()

class MembershipRole(Model, SerializerMixin):
    __tablename__ = 'membership_roles'
    __public__ = ('id', 'name', 'display_name')
    query_class = FilteredQuery
    name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Integer, default=0)
    users_for_role = db.relationship(
        'OrganizationMembership',
        back_populates='membership_role'
    )

    __mapper_args__ = {
        'order_by': name
    }

    @staticmethod
    def __insert_defaults():
        # this role has to exist
        roles = [['OrgAdmin', 'Administrator Organisation']]
        default_roles = [
           ['tech-c', 'Domain Technical Contact (tech-c)'],
           ['abuse-c', 'Domain Abuse Contact (abuse-c)'],
           ['billing-c', 'Domain Billing Contact (billing-c)'],
           ['admin-c', 'Domain Administrative Contact (admin-c)'],
           ['CISO', 'CISO'],
           ['private', 'Private'],
        ]

        try:
            stream = open('install/roles.yaml')
            data_loaded = yaml.load(stream, yaml.Loader)
            for role in data_loaded:
                roles.append([role['name'], role['display_name']])
        except IOError:
            for role in default_roles:
                roles.append(role)

        for r in roles:
            role = MembershipRole.query.filter_by(name=r[0]).first()

            if role is None:
                role = MembershipRole(name=r[0], display_name=r[1] )
                db.session.add(role)
        db.session.commit()

        def __repr__(self):
            return '{} #{}'.format(self.__class__.__name__, self.name)



class OrganizationMembership(Model, SerializerMixin):
    __tablename__ = 'organization_memberships'
    __public__ = ('id', 'user_id', 'organization_id', 'street', 'zip', 'city',
                  'country', 'comment', 'email', 'phone', 'mobile', 'membership_role_id',
                  'pgp_key_id', 'pgp_key_fingerprint', 'pgp_key', 'smime', 'country_id',
                  'coc', 'coc_filename', 'smime_filename')
    __table_args__ = (
        db.UniqueConstraint('user_id', 'organization_id', 'membership_role_id', 'deleted', name='role_unique'),
    )

    query_class = FilteredQuery
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="user_memberships", lazy='subquery')
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    # organization = db.relationship("Organization", back_populates="organization_membership")
    organization = db.relationship("Organization")
    membership_role_id = db.Column(db.Integer, db.ForeignKey('membership_roles.id'))
    membership_role = db.relationship("MembershipRole")
    street = db.Column(db.String(255))
    zip = db.Column(db.String(25))
    city = db.Column(db.String(255))
    # country = db.Column(db.String(50))  # should be a lookup table
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship("Country")
    comment = db.Column(db.String(255))
    _email = db.Column('email', db.String(255))
    _phone = db.Column('phone', db.String(255))
    _mobile = db.Column('mobile', db.String(255))
    deleted = db.Column(db.Integer, default=0)
    ts_deleted = db.Column(db.DateTime)
    pgp_key_id = db.Column(db.String(255))
    pgp_key_fingerprint = db.Column(db.String(255))
    pgp_key = deferred(db.Column(db.Text))
    smime = deferred(db.Column(db.Text))
    smime_filename = db.Column(db.String(255))
    coc = deferred(db.Column(db.Text))
    coc_filename = db.Column(db.String(255))

    # OrganisationMembership.mark_as_deleted
    def mark_as_deleted(self, delete_last_membership = False):
        mc = self.user.user_memberships_dyn.filter_by(deleted = 0)
        if mc.count() == 1 and delete_last_membership is False:
            raise AttributeError('Last membership may not be deleted')
        self.deleted = 1
        self.ts_deleted = datetime.datetime.utcnow()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email:
            email = email.lower()
            if not validate_email(email):
                raise AttributeError(email, 'seems not to be a valid email address')
            self._email = email
            return email
        self._email = None
        return None

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = check_phonenumber(phone)

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        self._mobile = check_phonenumber(mobile)

    @staticmethod
    def upsert(organization_membership_dict, membership = None):
        if membership:
            existing_membership_role_id = membership.membership_role_id
            if organization_membership_dict['membership_role_id'] ==\
                   existing_membership_role_id:
                check_role_id = -1
            else:
                check_role_id = existing_membership_role_id
        else:
            existing_membership_role_id = None
            check_role_id = organization_membership_dict['membership_role_id']

        # have to check constraint manually because sqlalchemy 
        # doesnt handle it properly in web context   
        check_constraint =  OrganizationMembership.query.filter( \
                 OrganizationMembership.membership_role_id == \
                            check_role_id,
                 OrganizationMembership.organization_id == \
                            organization_membership_dict['organization_id'],
                 OrganizationMembership.user_id == \
                            organization_membership_dict['user_id'],
                 OrganizationMembership.deleted == 0).first()

        if check_constraint:
            raise AttributeError('User already has this in role with this organization')
        
        try:
            if membership:
                membership.from_json(organization_membership_dict)
            else:
                membership = OrganizationMembership.fromdict(
                           organization_membership_dict)
        except IntegrityError:
            raise AttributeError('User already has this in role with this organization')
        message = 'Membership saved'
        httpcode = 201
        db.session.add(membership)
        admin_role = MembershipRole.query.filter_by(name = 'OrgAdmin').first()
        if membership.membership_role_id == admin_role.id and \
           existing_membership_role_id != admin_role.id:
            token = membership.user.generate_reset_token()
            send_email('energy-cert account', [membership.user.email],
                'auth/email/org_account_admin', org_mem=membership,
                token=token.decode("utf-8"))
             
        db.session.add(membership.user)
        return (membership, message)


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    user = User.query.get(int(user_id))
    if not user.login_timestamp:
        return None

    now = datetime.datetime.now()
    last_active = now - user.login_timestamp 

    # print('inactive', last_active.total_seconds())

    if last_active.total_seconds() > current_app.config['LOGOUT_INACTIVE_SECONDS'] + 60:
        user.login_timestamp = None
        db.session.add(user)
        db.session.commit()
        return None

    user.login_timestamp = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    return user

# @login_manager.token_loader
'''
def load_token(token):
    """
    Flask-Login token_loader callback.
    The token_loader function asks this function to take the token that was
    stored on the users computer process it to check if its valid and then
    return a User Object if its valid or None if its not valid.

    :param token: Token generated by :meth:`app.models.User.get_auth_token`
    """

    # The Token itself was generated by User.get_auth_token.  So it is up to
    # us to known the format of the token data itself.

    # The Token was encrypted using itsdangerous.URLSafeTimedSerializer which
    # allows us to have a max_age on the token itself.  When the cookie is
    # stored
    # on the users computer it also has a exipry date, but could be changed by
    # the user, so this feature allows us to enforce the exipry date of the
    # token
    # server side and not rely on the users cookie to exipre.

    max_age = current_app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
    # print("*****",  max_age)
    # Decrypt the Security Token, data = [username, hashpass, id]
    s = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt='user-auth',
        signer_kwargs=dict(key_derivation='hmac',
                           digest_method=hashlib.sha256))
    # from pprint import pprint
    try:
        (data, timestamp) = s.loads(token, max_age=max_age, return_timestamp=True)
        # pprint(data)
        # pprint(timestamp)
    except (BadTimeSignature, SignatureExpired):
        return None

    # Find the User
    user = User.query.get(data[2])

    # 2FA check
    totp_endpoint = request.endpoint == 'auth.verify_totp'
    if user and user.otp_enabled and not totp_endpoint and len(data) < 4:
        return None

    # Check Password and return user or None
    if user and data[1] == user._password:
        return user
    return None
'''


@login_manager.request_loader
def load_user_from_request(request):
    """Login users using api_key for header values
    See `<https://flask-login.readthedocs.org/en/latest/#custom-login-using-
    :param request: Flask request
    """
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_authorization')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            current_app.log.warn(
                "{} logged in using URL parameter".format(user.name)
            )
            return user

    # next, try to login using an API key
    api_key = request.headers.get('API-Authorization')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None
