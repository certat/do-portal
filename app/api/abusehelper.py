from flask import request, current_app, url_for
from flask_jsonschema import validate
from .. import db
from ..models import AHBot as Bot
from .decorators import json_response
from . import api


@api.route('/abusehelper', methods=['GET'])
@json_response
def get_abusehelper():
    """Return a list of available abusehelper

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/abusehelper HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "abusehelper": [
            {
              "name": "ShadowServerBot",
              "url": "http://sample.com/path.html",
              "id": 1
            }
          ]
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json array abusehelper: List of available bots
    :>jsonobj integer id: Bot ID
    :>jsonobj integer name: Bot name

    :status 200: Deliverable endpoint found, response may be empty
    :status 404: Not found
    """
    bots = Bot.query.filter().all()
    return {'abusehelper': [a.serialize() for a in bots]}


@api.route('/abusehelper/<int:bot_id>', methods=['GET'])
@json_response
def get_got(bot_id):
    """Get bot from database

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/abusehelper/1 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "name": "ShadowServerBot",
          "url": "http://sample.com/path.html",
          "id": 1
        }

    :param bot_id: Bot unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Bot unique ID
    :>json integer name: Bot name

    :status 200: ASN found
    :status 404: Resource not found
    """
    a = Bot.query.get_or_404(bot_id)
    return a.serialize()


@api.route('/abusehelper', methods=['POST', 'PUT'])
@validate('abusehelper', 'add_bot')
@json_response
def add_bot():
    """Add new bot entry

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/abusehelper HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "name": "ShadowServerBot",
          "url": "http://sample.com/path.html"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "bot": {
            "name": "ShadowServerBot",
            "url": "http://sample.com/path.html",
            "id": 1
          },
          'message': "Bot added"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json integer name: Bot name
    :>jsonobj integer id: Unique ID of new bot
    :>jsonobj integer name: bot name
    :>json string message: Status message

    :status 201: ASN successfully saved
    :status 400: Bad request
    """
    a = Bot.fromdict(request.json)
    db.session.add(a)
    db.session.commit()
    return {'bot': a.serialize(), 'message': 'Bot added'}, 201, \
           {'Location': url_for('api.get_bot', bot_id=a.id)}


@api.route('/abusehelper/<int:bot_id>', methods=['PUT'])
@validate('abusehelper', 'update_bot')
@json_response
def update_bot(bot_id):
    return NotImplemented


@api.route('/abusehelper/<int:bot_id>', methods=['DELETE'])
@json_response
def delete_bot(bot_id):
    """Delete bot

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/abusehelper/1 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Bot deleted"
        }

    :param bot_id: Bot unique ID.

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: Bot was deleted
    :status 404: Bot was not found
    """
    a = Bot.query.filter_by(id == bot_id).delete()
    if not a:
        return {'message': 'No such bot'}, 404
    db.session.commit()
    return {'message': 'Bot deleted'}


@api.route('/abusehelper', methods=['DELETE'])
@json_response
def delete_abusehelper():
    """Clear abusehelper table

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/abusehelper HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Bots deleted"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: Bot was deleted
    :status 404: Bot was not found
    """
    a = Bot.query.all().delete()
    db.session.commit()
    current_app.log.debug('Deleted {} abusehelper'.format(a))
    return {'message': 'Bots deleted'}
