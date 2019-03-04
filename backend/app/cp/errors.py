from flask_jsonschema import ValidationError
from sqlalchemy.exc import IntegrityError
from app.core import ApiResponse
from app.api.errors import forbidden, unauthorized, not_found
from app.api.errors import not_acceptable  # noqa
from . import cp


@cp.errorhandler(IntegrityError)
def server_error(e):
    return ApiResponse({'message': e.args[0]}, 500)


@cp.errorhandler(401)
def unauthorized_handler(e):
    return unauthorized('Unauthorized')


@cp.errorhandler(403)
def forbidden_handler(e):
    return forbidden('You don\'t have the permission to access the requested'
                     ' resource. It is either read-protected or not readable '
                     'by the server.')


@cp.errorhandler(404)
def not_found_handler(e):
    return not_found('Resource not found')


@cp.errorhandler(ValidationError)
def on_validation_error(e):
    return ApiResponse({'message': e.message, 'validator': e.validator}, 422)
