import csv
from io import StringIO
from flask import send_file, make_response
from flask_login import login_required
from . import main
from ..models import IpRange
from ..api import ip_ranges


@main.route('/')
def index():
    return send_file('templates/index.html')


@main.route('/export', defaults={'export_format': 'csv'})
@main.route('/export/<string:export_format>')
@login_required
def export(export_format):
    ranges = IpRange.query.filter(IpRange.deleted == 0).all()
    if export_format == 'csv':
        si = StringIO()
        cw = csv.writer(si)
        for ip_range in ranges:
            cw.writerow([ip_range.ip_range])
        out = make_response(si.getvalue())
        out.headers["Content-Disposition"] = "attachment; filename=export.csv"
        out.headers["Content-type"] = "text/csv"
        return out
    elif export_format == 'json':
        return ip_ranges.get_ip_ranges()
