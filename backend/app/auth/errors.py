from itsdangerous import BadSignature, BadTimeSignature
from sqlalchemy.exc import IntegrityError
from flask_jsonschema import ValidationError
from app.api.decorators import json_response
from app.api.errors import forbidden
from app.api.errors import not_acceptable  # noqa
from . import auth


@auth.errorhandler(IntegrityError)
@json_response
def server_error(e):
    return {'message': e.args[0]}, 500


@auth.errorhandler(403)
def forbidden_handler(e):
    return forbidden('You don\'t have the permission to access the requested'
                     ' resource. It is either read-protected or not readable '
                     'by the server.')


@auth.errorhandler(ValidationError)
@json_response
def on_validation_error(e):
    return {'message': e.message, 'validator': e.validator}, 422


@auth.errorhandler(BadTimeSignature)
@json_response
def on_bad_time_signature(e):
    return {'message': e.args[0], 'validator': 'signature'}, 400


@auth.errorhandler(BadSignature)
@json_response
def on_bad_signature(e):
    return {'message': e.args[0]}, 400
