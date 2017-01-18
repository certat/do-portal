import os
import json
import gzip
from io import BytesIO, StringIO
from flask import url_for
from flask_tinyclients.vxstream import VxAPIClient
from flask_sqlalchemy import BaseQuery
from app.models import User
from tests import DOTestCase
from tests import create_sample
from app import vxstream
from app.api.analysis.vxstream import _state_to_name, SUCCESS
from unittest.mock import patch, Mock, MagicMock


class VxStreamTestCase(DOTestCase):

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
            url_for('api.add_sample'),
            data=dict(file=(sample.data, sample.filename)),
            headers=self.get_req_headers(),
            content_type='multipart/form-data'
        )

    @patch('tests.test_vxstream.vxstream.submit')
    def test_submit_sample_for_vxstream_analysis(self, vxstream_submit):
        vxstream_submit.return_value = {
            'response_code': 0,
            'response': 'Mocked response'
        }
        sample = create_sample(b'clean')
        rv = self.client.post(
            url_for('api.add_sample'),
            data=dict(file=(sample.data, sample.filename)),
            headers=self.get_req_headers(),
            content_type='multipart/form-data'
        )
        self.assertTrue(rv.status_code == 201)
        json_rv = json.loads(rv.data.decode('utf-8'))
        self.assertTrue(
            json_rv['files'][0]['sha256'] == sample.sha256)

        json_rv['dyn_analysis'] = {"vxstream": [5, 6]}
        rv = self.client.post(
            url_for('api.add_vxstream_analysis'),
            data=json.dumps(json_rv),
            headers=self.get_req_headers()
        )

        self.assertJSONMsg(
            rv, rv_status=202,
            value='Your files have been submitted for dynamic analysis')

    @patch('tests.test_vxstream.vxstream.submiturl')
    def test_submit_url(self, vxstream_submit):
        vxstream_submit.return_value = {
            'response_code': 0,
            'response': {
                'sha256': 'b291588f2d2b3546a53694e56c6b801ab436fa7bc6ecc71953b69fd1d450ca9b'
            }
        }
        rv = self.client.post(
            url_for('api.add_vxstream_url_analysis'),
            data=json.dumps(dict(
                urls=['https://cert.europa.eu'],
                dyn_analysis=dict(vxstream=[1])
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, key='message', rv_status=202,
            value='Your URLs have been submitted for dynamic analysis')

    @patch('tests.test_vxstream.vxstream.state')
    def test_get_vxstream_envs(self, vxstream_state):
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
            url_for('api.get_vxstream_environments'),
            headers=self.get_req_headers()
        )

        self.assertJSONIsNotNone(rv, key='environments')

    def test_get_vxstream_local_reports(self):
        rv = self.client.get(
            url_for('api.get_vxstream_analyses'),
            headers=self.get_req_headers()
        )
        self.assertTrue('DO-Page-Item-Count' in rv.headers)
        self.assertJSONIsNotNone(rv, key='items')

    @patch.object(VxAPIClient, 'get')
    def test_get_html_report(self, mock_report):
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)

        fgz = BytesIO()
        with gzip.GzipFile('report.gz', mode='wb', fileobj=fgz) as gzipobj:
            gzipobj.write(b'<html><head></head></html>')
        mock_report.return_value = bytes(fgz)
        rv = self.client.get(
            url_for(
                'api.get_vxstream_report',
                sha256=sample.sha256,
                envid=1, type='html'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch.object(VxAPIClient, 'get')
    def test_get_json_report(self, mock_report):
        # :fixme:
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)
        mock_report.return_value = json.dumps({
            'report': 'blah'
        })
        rv = self.client.get(
            url_for(
                'api.get_vxstream_report',
                sha256=sample.sha256,
                envid=1, type='json'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch.object(VxAPIClient, 'get')
    @patch.object(BaseQuery, 'first_or_404')
    def test_get_vxstream_json_summary(self, mock_sample, vxstream_get):
        sample = create_sample(b'clean')
        mock_sample.return_value = sample
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
            url_for('api.get_vxstream_analysis',
                    sha256=sample.sha256, envid=1),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'response_code', 0)
        os.unlink(os.path.join(
            self.app.config['APP_UPLOADS_SAMPLES'],
            sample.sha256)
        )

    @patch.object(VxAPIClient, 'get')
    def test_download_html_report(self, mock_report):
        sample = create_sample(b'clean')
        saved_sample = self._save_sample(sample)
        self.assertTrue(saved_sample.status_code == 201)

        fgz = BytesIO()
        with gzip.GzipFile('report.gz', mode='wb', fileobj=fgz) as gzipobj:
            gzipobj.write(b'<html><head></head></html>')
        mock_report.return_value = bytes(fgz)
        rv = self.client.get(
            url_for(
                'api.get_vxstream_download',
                sha256=sample.sha256,
                eid=1, ftype='html'
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
