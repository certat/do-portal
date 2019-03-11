from flask import g, request, abort
from app.core import ApiResponse
from app import db
from . import cp
from flask import Response, current_app
import requests
from app.models import Organization, FodyOrganization
import flask_cors

# /statistics?orgid=123
@cp.route('/statistics/', methods=['GET'])
def get_grafana_by_id(org_id):
    orgid = request.args.get('orgid', type = int)
    response = Response('<p>bla orgid:'+orgid+'</p>', 200, headers)


@cp.route('/statistics/', methods=['GET'])
@flask_cors.cross_origin()
def get_grafana():
    orgid = 5
    o = Organization.query.get_or_404(orgid)
    if not g.user.may_handle_organization(o):
        abort(403)

    ripe_handles = o.ripe_organizations
    asns = [FodyOrganization(r.ripe_org_hdl).asns for r in ripe_handles]
    # http://localhost:3005/d/QA7iWe9iz/teshboard?orgId=1&asn=1
    grafana_url = ("%s:%s/%s/%s?%s" % (
       current_app.config['GRAFANA_HOST'],
       current_app.config['GRAFANA_PORT'],
       current_app.config['GRAFANA_ID'],
       current_app.config['GRAFANA_DASHBOARDNAME'],
       current_app.config['GRAFANA_OPTIONS'],
    ))
    for asn in asns:
       grafana_url += '&var-asn='+asn[0]

    # asns.append(grafana_url)
    # return ApiResponse(asns)

    request_headers = {key: value for (key, value) in request.headers  if key != 'Host'}
    request_headers['X_GRAFANA_REMOTE_USER'] =  current_app.config['GRAFANA_REMOTE_USER']
    resp = requests.request(
        method=request.method,
        url=grafana_url,  # request.url.replace(request.host_url, 'orf.at'),
        headers=request_headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    c = resp.content.decode('utf-8')
    content = c.replace("/grafana/", "http://localhost:3005/grafana/")
    response = Response(content, resp.status_code, headers)
    # headers = []
    # response = Response('<p> bla </p>', 200, headers)

    return response

'''
GRAFANA_HOST=localhost
GRAFANA_PORT=3005
GRAFANA_ID='d/QA7iWe9iz/'
GRAFANA_DASHBOARDNAME=teshboard
GRAFANA_OPTIONS='orgId=1'
GRAFANA_REMOTE_USER=dope
'''
