import os
import gzip
from collections import namedtuple
from io import BytesIO
import hashlib
import json
from unittest.mock import patch
import ssdeep
from flask import url_for, g
from flask_tinyclients.vxstream import VxAPIClient
from app import vxstream
from unittest.mock import Mock
from app.models import User
from app.api.analysis.vxstream import _state_to_name, SUCCESS
from tests import DOTestCase
from tests import create_sample


class CPTestCase(DOTestCase):

    current_user = None

    def setUp(self):
        super().setUp()
        self.current_user = User.create_test_user()
        self.login(self.current_user.email)

    def tearDown(self):
        self.current_user = None
        super().tearDown()

    def _save_sample(self, sample):
        return self.client.post(
            url_for('cp.add_cp_sample'),
            data=dict(file=(sample.data, sample.filename)),
            headers=self.get_req_headers(),
            content_type='multipart/form-data'
        )

    def create_organization(self):
        return self.client.post(
            url_for('api.add_organization'),
            data=json.dumps(dict(
                abbreviation="CERT-EU",
                full_name="Computer Emergency Response Team for EU "
                          "Institutions Agencies and Bodies",
                ip_ranges=["212.8.189.16/28"],
                abuse_emails=["cert-eu@ec.europa.eu"],
                contact_emails=[{"email": self.current_user.email}],
                asns=[5400],
                fqdns=["cert.europa.eu"]
            )),
            headers=self.get_req_headers()
        )

    def test_get_cp_organization(self):
        self.login(self.current_user.email)
        rv = self.create_organization()
        json_rv = json.loads(rv.data.decode('utf-8'))
        self.current_user.organization_id = json_rv['organization']['id']
        rv = self.client.get(
            url_for('cp.get_cp_organization'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'abbreviation')

    def test_update_cp_organization(self):
        self.login(self.current_user.email)
        rv = self.create_organization()
        json_rv = json.loads(rv.data.decode('utf-8'))
        self.current_user.organization_id = json_rv['organization']['id']

        rv = self.client.put(
            url_for('cp.update_cp_organization', org_id=1),
            data=json.dumps(dict(
                abbreviation="CERT-EU",
                full_name="Updated name",
                ip_ranges=["212.8.189.17/28"],
                abuse_emails=["cert-eu@ec.europa.eu"],
                contact_emails=[{"email": self.current_user.email}],
                asns=[5400],
                fqdns=["cert.europa.eu"]
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', 'Organization saved')

    def test_get_cp_samples(self):
        rv = self.client.get(
            url_for('cp.get_samples'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    def test_cp_add_sample(self):
        cpsample = create_sample(b'cpsample')
        rv = self._save_sample(cpsample)
        self.assertTrue(rv.status_code == 201)
        json_rv = json.loads(rv.data.decode('utf-8'))

        self.assertTrue(
            json_rv['files'][0]['sha256'] == cpsample.sha256)

    @patch('tests.test_cp.vxstream.state')
    def test_get_cp_vxstream_environments(self, vxstream_state):
        vxstream_state.return_value = {
            'response_code': 0,
            'response': {
                'environmentList': {
                    1: 'Windows 7 64 bit',
                    5: 'Windows 7 32 bit (KERNELMODE)',
                    6: 'Windows 7 64 bit (KERNELMODE)'
                }
            }
        }

        rv = self.client.get(
            url_for('cp.get_cp_vxstream_environments'),
            headers=self.get_req_headers()
        )

        self.assertJSONIsNotNone(rv, key='environments')

    @patch('tests.test_cp.vxstream.submit')
    def test_submit_cpsample_for_vxstream_analysis(self, vxstream_submit):
        vxstream_submit.return_value = {
            'response_code': 0,
            'response': 'Mocked response'
        }
        cpsample = create_sample(b'cpsample')
        rv = self._save_sample(cpsample)
        self.assertTrue(rv.status_code == 201)
        json_rv = json.loads(rv.data.decode('utf-8'))

        self.assertTrue(
            json_rv['files'][0]['sha256'] == cpsample.sha256)

        json_rv['dyn_analysis'] = {"vxstream": [5, 6]}
        rv = self.client.post(
            url_for('cp.add_cp_vxstream_analysis'),
            data=json.dumps(json_rv),
            headers=self.get_req_headers()
        )

        self.assertJSONMsg(
            rv, rv_status=202,
            value='Your files have been submitted for dynamic analysis')

        os.unlink(os.path.join(
            self.app.config['APP_UPLOADS_SAMPLES'],
            cpsample.sha256)
        )

    def test_get_cp_av_engines(self):
        self.login(self.current_user.email)
        rv = self.client.get(
            url_for('cp.get_cp_av_engines'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, key='engines')

    def test_add_cp_av_scan(self):
        self.login(self.current_user.email)
        sample = create_sample(b'cpsampleforav', filename='av.zip')
        rv = self._save_sample(sample)
        self.assertTrue(rv.status_code == 201)
        json_rv = json.loads(rv.data.decode('utf-8'))

        self.assertTrue(
            json_rv['files'][0]['sha256'] == sample.sha256)

        rv = self.client.post(
            url_for('cp.add_cp_av_scan'),
            data=json.dumps(json_rv),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, value='Your files have been submitted for AV scanning',
            rv_status=202
        )

        os.unlink(os.path.join(
            self.app.config['APP_UPLOADS_SAMPLES'],
            sample.sha256)
        )

        rv = self.client.get(
            url_for('cp.get_sample', sha256=sample.sha256),
            headers=self.get_req_headers())
        self.assertJSONMsg(rv, 'sha256', sample.sha256)

        rv = self.client.get(
            url_for('cp.get_cp_av_scan', sha256=sample.sha256),
            headers=self.get_req_headers())
        self.assertTrue(rv.status_code == 404)

    @patch.object(VxAPIClient, 'get')
    def test_get_cp_vxstream_json_summary(self, vxstream_get):
        sample = create_sample(b'cpclean')
        rv = self._save_sample(sample)
        self.assertTrue(rv.status_code == 201)
        state_resp = Mock(
            return_value={
                'response': {'state': _state_to_name[SUCCESS]},
                'response_code': 0
            }
        )
        summary_resp = Mock(
            return_value={
                'response': {
                    "analysis_start_time": "2016-05-11 21:50:33",
                    "domains": [],
                    "environmentDescription": "Windows 7 x64 (Stealth)",
                    "environmentId": "6",
                    "hosts": [],
                    "isinteresting": False,
                    "isurlanalysis": False,
                    "md5": sample.md5,
                    "sha1": sample.sha1,
                    "sha256": sample.sha256,
                    "size": 26616,
                    "targeturl": "",
                    "threatlevel": 0,
                    "threatscore": 0,
                    "type": "PE32 executable (native) Intel 80386"
                },
                'response_code': 0
            }
        )
        vxstream_get.side_effect = [
            state_resp(),
            summary_resp()
        ]

        rv = self.client.get(
            url_for('cp.get_cp_vxstream_analysis',
                    sha256=sample.sha256, envid=6),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'response_code', 0)

    def test_cp_start_static_analysis(self):
        rv = self.client.post(
            url_for('cp.add_cp_analysis'),
            data=json.dumps(dict(files=[{'sha256': '1eedab2b09a4bf6c'}])),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, key='message', rv_status=202,
            value='Your files have been submitted for static analysis')

    def test_get_cp_static_analysis(self):
        rv = self.client.get(
            url_for('cp.get_cp_analysis', sha256='1eeb2b09a4bf6c87b273305c09'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 404)

    @patch.object(VxAPIClient, 'get')
    def test_get_cp_html_report(self, mock_report):
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)

        fgz = BytesIO()
        with gzip.GzipFile('report.gz', mode='wb', fileobj=fgz) as gzipobj:
            gzipobj.write(b'<html><head></head></html>')
        mock_report.return_value = bytes(fgz)
        rv = self.client.get(
            url_for(
                'cp.get_cp_vxstream_report',
                sha256=sample.sha256,
                envid=1, type='html'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch.object(VxAPIClient, 'get')
    def test_get_json_report(self, mock_report):
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)
        mock_report.return_value = json.dumps({
            'report': 'blah'
        })
        rv = self.client.get(
            url_for(
                'cp.get_cp_vxstream_report',
                sha256=sample.sha256,
                envid=1, type='json'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch.object(VxAPIClient, 'get')
    def test_download_cp_html_report(self, mock_report):
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)

        fgz = BytesIO()
        with gzip.GzipFile('report.gz', mode='wb', fileobj=fgz) as gzipobj:
            gzipobj.write(b'<html><head></head></html>')
        mock_report.return_value = bytes(fgz)
        rv = self.client.get(
            url_for(
                'cp.get_cp_vxstream_download',
                sha256=sample.sha256,
                eid=1, ftype='html'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch('tests.test_cp.vxstream.submiturl')
    def test_submit_url(self, vxstream_submit):
        vxstream_submit.return_value = {
            'response_code': 0,
            'response': {
                'sha256': 'b291588f2d2b3546a53694e56c6b801ab436fa7bc6ecc71953b69fd1d450ca9b'
            }
        }
        rv = self.client.post(
            url_for('cp.add_cp_vxstream_url_analysis'),
            data=json.dumps(dict(
                urls=['https://cert.europa.eu'],
                dyn_analysis=dict(vxstream=[1])
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, key='message', rv_status=202,
            value='Your URLs have been submitted for dynamic analysis')
