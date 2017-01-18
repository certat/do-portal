from flask_jsonschema import validate
from .decorators import json_response
from . import api


@api.route('/gnupg-keys', methods=['GET'])
@json_response
def get_gnupg_keys():
    """

    :status 501: NotImplemented
    """
    return {'gnupg-keys': []}, 501


@api.route('/gnupg-keys/<string:key_id>', methods=['GET'])
@json_response
def get_gnupg_key(key_id):
    """

    :status 501: NotImplemented
    """
    return {}, 501


@api.route('/gnupg-keys', methods=['POST', 'PUT'])
@validate('gnupg', 'submit_key')
@json_response
def add_gnupg_key():
    """

    :status 501: NotImplemented
    """
    return {}, 501


@api.route('/gnupg-keys/<string:key_id>', methods=['PUT'])
@validate('gnupg', 'update_key')
@json_response
def update_gnupg_key(key_id):
    """

    :status 501: NotImplemented
    """
    return {'message': 'GnuPG key saved'}, 501


@api.route('/gnupg-keys/<string:key_id>', methods=['DELETE'])
@json_response
def delete_gnupg_key(key_id):
    """

    :status 501: NotImplemented
    """
    return {'message': 'GnuPG key deleted'}, 501
