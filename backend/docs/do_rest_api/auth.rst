.. _auth:

Authentication
==============

Making authenticated requests using the ``API-Authorization`` header:

**Example request**

.. sourcecode:: http

    GET /api/1.0/organizations HTTP/1.1
    Host: do.cert.europa.eu
    Accept: application/json
    Content-Type: application/json
    API-Authorization: ad6bfbb0df17c1f2a7cbe1548444803d6114b8d877e37dd4f

.. note::

    ``API-Authorization`` is your API key found in the ``My Account`` section.

**Example success response**

.. sourcecode:: http

    HTTP/1.0 200 OK
    Content-Type: application/json

    {
      "organizations": "..."
    }

**Example error response**

.. sourcecode:: http

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: application/json

    {
      "message": "Unauthorized",
      "status": "unauthorized"
    }

Statuses
--------

* :http:statuscode:`200`: Request was successful
* :http:statuscode:`401`: Authorization failure. The client MAY repeat the
  request with a suitable API-Authorization header field. If the request
  already included Authorization credentials, then the 401 response indicates
  that authorization has been refused for those credentials.
* :http:statuscode:`403`: Access denied. Authorization will not help and the
  request SHOULD NOT be repeated.
* :http:statuscode:`400`: General client failure
* :http:statuscode:`500`: General server failure


Authentication endpoints
------------------------

.. autoflask:: app:create_app('default')
    :undoc-static:
    :blueprints: auth
    :modules: app.auth.routes