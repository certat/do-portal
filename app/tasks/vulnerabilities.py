import requests
import datetime
from app import celery, db
from app.models import Vulnerability


@celery.task
def checkall(checked_patched=False):
    if checked_patched:
        vulns = Vulnerability.query.all()
    else:
        vulns = Vulnerability.query.filter_by(patched=None).all()

    for vuln in vulns:
        resp = requests.request(vuln.request_method, vuln.url,
                                data=vuln.request_data,
                                allow_redirects=False)
        if vuln.check_string not in resp.text:
            vuln.patched = datetime.datetime.now()
        else:
            vuln.patched = None

        vuln.updated = datetime.datetime.now()
        db.session.add(vuln)
    db.session.commit()
