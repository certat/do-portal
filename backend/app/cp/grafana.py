from flask import g, request, abort
from app.core import ApiResponse
from app import db
from . import cp
from flask import Response
import requests


@cp.route('/statistics', methods=['GET'])
def get_grafana():
    request_headers = {key: value for (key, value) in request.headers  if key != 'Host'}
    request_headers['X_GRAFANA_REMOTE_USER'] = 'dope'
    resp = requests.request(
        method=request.method,
        url='http://orf.at',  # request.url.replace(request.host_url, 'orf.at'),
        headers=request_headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response


