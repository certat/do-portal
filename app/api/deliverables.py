from flask import request, redirect, url_for
from . import api
from ..import db
from ..models import Deliverable
from .decorators import json_response
from flask_jsonschema import validate


@api.route('/deliverables', methods=['GET'])
@json_response
def get_deliverables():
    """Return a list of available deliverables

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/deliverables HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "deliverables": [
            {
              "id": 1,
              "name": "CITAR"
            },
            {
              "id": 2,
              "name": "CIMBL"
            }
          ]
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json array deliverables: List of available deliverables objects
    :>jsonobj integer id: Deliverable unique ID
    :>jsonobj string name: Deliverable name

    :status 200: Deliverable endpoint found, response may be empty
    :status 404: Not found
    """
    deliverables = Deliverable.query.all()
    return {'deliverables': [o.serialize() for o in deliverables]}


@api.route('/deliverables/<int:deliverable_id>', methods=['GET'])
@json_response
def get_deliverable(deliverable_id):
    """Get deliverable from database

    **Example request**:

    .. sourcecode:: http

        GET /api/1.0/deliverables/2 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "id": 2,
          "name": "CITAR"
        }

    :param deliverable_id: deliverable unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json integer id: Deliverable unique ID
    :>json string name: Deliverable name

    :status 200: File found
    :status 404: Resource not found
    """
    g = Deliverable.query.get_or_404(deliverable_id)
    return g.serialize()


@api.route('/deliverables', methods=['POST', 'PUT'])
@validate('deliverables', 'add_deliverable')
@json_response
def add_deliverable():
    """Create new deliverable type

    **Example request**:

    .. sourcecode:: http

        POST /api/1.0/deliverables HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "active": true,
          "name":"test"
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: application/json

        {
          "deliverable": {
            "id": 4,
            "name": "test"
          },
          "message": "Deliverable added"
        }

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json string name: Name of new deliverable
    :<json boolean active: Actively used
    :>jsonobj integer id: Unique ID of new deliverable
    :>jsonobj string name: Name of deliverable
    :>json string message: Status message

    :status 201: Deliverable successfully saved
    :status 400: Bad request
    """
    g = Deliverable().from_json(request.json)
    db.session.add(g)
    db.session.commit()
    return {'deliverable': g.serialize(), 'message': 'Deliverable added'}, \
        201, {'Location': url_for('api.get_deliverable', deliverable_id=g.id)}


@api.route('/deliverables/<int:deliverable_id>', methods=['PUT'])
@validate('deliverables', 'update_deliverable')
@json_response
def update_deliverable(deliverable_id):
    """Update deliverable

    **Example request**:

    .. sourcecode:: http

        PUT /api/1.0/deliverables/4 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json
        Content-Type: application/json

        {
          "id": 4,
          "name": "test-updated",
          "active":true
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Deliverable saved"
        }

    :param deliverable_id: Deliverable unique ID

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :<json integer id: Unique ID of deliverable
    :<json string name: Name of deliverable
    :<json boolean active: Actively used
    :>json string message: Status message

    :status 200: Deliverable was successfully updated
    :status 400: Bad request
    """
    g = Deliverable.query.filter(
        Deliverable.id == deliverable_id
    ).first()
    if not g:
        return redirect(url_for('api.add_deliverable'))
    g.from_json(request.json)
    db.session.add(g)
    db.session.commit()
    return {'message': 'Deliverable saved'}


@api.route('/deliverables/<int:deliverable_id>', methods=['DELETE'])
@json_response
def delete_deliverable(deliverable_id):
    """Delete deliverable type

    **Example request**:

    .. sourcecode:: http

        DELETE /api/1.0/deliverables/4 HTTP/1.1
        Host: do.cert.europa.eu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "message": "Deliverable deleted"
        }

    :param deliverable_id: file's unique ID.

    :reqheader Accept: Content type(s) accepted by the client
    :resheader Content-Type: this depends on `Accept` header or request

    :>json string message: Action status status

    :status 200: Deliverable was deleted
    :status 404: Deliverable was not found
    """
    g = Deliverable.query.filter(
        Deliverable.id == deliverable_id
    ).first()
    if not g:
        return {'message': 'No such deliverable'}, 404

    g.deleted = 1
    db.session.add(g)
    db.session.commit()
    return {'message': 'Deliverable deleted'}
