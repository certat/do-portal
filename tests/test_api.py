from io import BytesIO
from flask import url_for
from .conftest import assert_msg


def test_api_routes_list(client):
    rv = client.get(url_for('api.api_index'))
    assert_msg(rv, key='endpoints')


def test_get_samples(client):
    rv = client.get(url_for('api.get_samples'))
    assert_msg(rv, key='items')


def test_get_sample(client):
    rv = client.get(url_for('api.get_sample', sha256=1))
    assert rv.status_code == 404


def test_add_sample(client, malware_sample):
    rv = client.post(
        url_for('api.add_sample'),
        data=dict(file=(BytesIO(), malware_sample.filename)),
        content_type='multipart/form-data'
    )
    assert rv.status_code == 201


def test_404(client):
    rv = client.get('/api/1.0/non-existent-resource')
    assert rv.status_code == 404


def test_teapot(client):
    rv = client.get(url_for('api.teapot'))
    assert_msg(rv, value="I'm a teapot", response_code=418)


def test_honeytoken(client):
    rv = client.get(url_for('api.api_honeytoken'))
    assert_msg(rv, value='No such user')
        # update organization
        rv = self.client.put(
            url_for('api.update_organization', org_id=1),
            data=json.dumps(dict(
                abbreviation="CERT-EU",
                full_name="Computer Emergency Response Team for EU "
                          "Institutions Agencies and Bodies",
                ip_ranges=["212.8.189.17/28"],
                abuse_emails=["cert-eu@ec.europa.eu"],
                contact_emails=[{"email": "cert-eu@ec.europa.eu"}],
                asns=[5400],
                fqdns=["cert.europa.eu"]
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # check organization
        rv = self.client.put(
            url_for('api.check_constituents'),
            data=json.dumps(["212.8.189.18", "1.2.3.4"]),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        json_data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(json_data["response"]["212.8.189.18"], "CERT-EU")

        # delete organization
        rv = self.client.delete(
            url_for('api.delete_organization', org_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Organization deleted')

        rv = self.client.delete(
            url_for('api.delete_organization', org_id=666),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 404)

    def test_organization_groups(self):
        rv = self.client.get(
            url_for('api.get_groups'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # create group
        rv = self.client.post(
            url_for('api.add_group'),
            data=json.dumps(dict(
                name="Test Group",
                color="#ffffff"
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

        # get group
        rv = self.client.get(
            url_for('api.get_group', group_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, key='name')

        # update group
        rv = self.client.put(
            url_for('api.update_group', group_id=1),
            data=json.dumps(dict(
                name="Test Group updated",
                color="#ff00ff"
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # delete group
        rv = self.client.delete(
            url_for('api.delete_group', group_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    def test_asns(self):
        self.create_organization()
        rv = self.client.get(
            url_for('api.get_asns'),
            headers=self.get_req_headers()
        )
        self.assertEqual(rv.status_code, 200)

        # create ASN
        rv = self.client.post(
            url_for('api.add_asn'),
            data=json.dumps(dict(asn=1234, organization_id=1, as_name="Dummy")),
            headers=self.get_req_headers()
        )
        self.assertEqual(rv.status_code, 201)

        # update ASN
        rv = self.client.put(
            url_for('api.update_asn', asn_id=1),
            data=json.dumps(dict(asn=1234, organization_id=1, as_name="Dummy")),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # delete ASN
        rv = self.client.delete(
            url_for('api.delete_asn', asn_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    def test_ip_ranges(self):
        self.create_organization()
        rv = self.client.get(
            url_for('api.get_ip_ranges'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # create IP range
        rv = self.client.post(
            url_for('api.add_ip_range'),
            data=json.dumps(dict(ip_range='1.2.3.4/24', organization_id=1)),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='IP range added', rv_status=201)

        # get IP range
        rv = self.client.get(
            url_for('api.get_ip_range', range_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'ip_range')

        # update IP range
        rv = self.client.put(
            url_for('api.update_ip_range', range_id=1),
            data=json.dumps(dict(ip_range='4.3.2.1/24', organization_id=1)),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='IP range saved')

        # delete IP range
        rv = self.client.delete(
            url_for('api.delete_ip_range', range_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    def test_fqdns(self):
        self.create_organization()
        rv = self.client.get(
            url_for('api.get_fqdns'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # create FQDN
        rv = self.client.post(
            url_for('api.add_fqdn'),
            data=json.dumps(dict(fqdn='cert.europa.eu', organization_id=1)),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

        # get FQDN
        rv = self.client.get(
            url_for('api.get_fqdn', fqdn_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # update FQDN
        rv = self.client.put(
            url_for('api.update_fqdn', fqdn_id=1),
            data=json.dumps(dict(fqdn='cert.europa.eu', organization_id=1)),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # delete FQDN
        rv = self.client.delete(
            url_for('api.delete_fqdn', fqdn_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    def test_deliverables(self):
        rv = self.client.get(
            url_for('api.get_deliverables'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # create deliverable
        rv = self.create_deliverable()
        self.assertTrue(rv.status_code == 201)

        # get deliverable
        rv = self.client.get(
            url_for('api.get_deliverable', deliverable_id=1),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, key='name', value='Sample deliverable')

        rv = self.client.get(
            url_for('api.get_deliverable', deliverable_id=666),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 404)

        # update deliverable
        rv = self.client.put(
            url_for('api.update_deliverable', deliverable_id=1),
            data=json.dumps(dict(
                name="Sample deliverable updated"
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Deliverable saved')

        # delete deliverable
        rv = self.client.delete(
            url_for('api.delete_deliverable', deliverable_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        rv = self.client.get(
            url_for('api.delete_deliverable', deliverable_id=666),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Resource not found', rv_status=404)

    def test_deliverable_files(self):
        rv = self.client.get(
            url_for('api.get_files'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # create deliverable
        rv = self.create_deliverable()
        self.assertTrue(rv.status_code == 201)

        # create deliverable file
        rv = self.client.post(
            url_for('api.add_file'),
            data=json.dumps(dict(
                files=["file.ext", "file2.ext"],
                deliverable_id=1)
            ),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

        # get file
        rv = self.client.get(
            url_for('api.get_file', file_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        json_data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(json_data['name'], "file.ext")

        rv = self.client.get(
            url_for('api.get_file', file_id=666),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 404)

        # delete file
        rv = self.client.delete(
            url_for('api.delete_file', file_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        rv = self.client.get(
            url_for('api.delete_file', file_id=666),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Resource not found', rv_status=404)


    @patch.object(MailmanQuery, 'all')
    def test_emails(self, muser):
        muser.return_value = [
            MagicMock(addresses=[
                MagicMock(__str__=lambda x: 'some-mail@ec.europa.eu'),
                MagicMock(__str__=lambda x: 'blahblah@domain.tld'),
            ])
        ]
        rv = self.client.get(
            url_for('api.get_emails'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'emails')

        # create organization, it will create an Email
        rv = self.create_organization()
        self.assertTrue(rv.status_code == 201)

        # update email
        rv = self.client.put(
            url_for('api.update_email', email_id=1),
            data=json.dumps(dict(
                email="updated-email@cert.europa.eu"
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Email saved')

        # delete email
        rv = self.client.delete(
            url_for('api.delete_email', email_id=1),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
        rv = self.client.get(
            url_for('api.delete_email', email_id=666),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Resource not found', rv_status=404)

    def test_av_scans(self):
        rv = self.client.get(
            url_for('api.get_av_scans'),
            headers=self.get_req_headers())
        self.assertTrue(rv.status_code == 200)

        rv = self.client.get(
            url_for('api.get_av_engines'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, key='engines')

        sample = create_sample(b'sampleforav', filename='av.zip')
        rv = self.client.post(
            url_for('api.add_sample'),
            data=dict(file=(sample.data, sample.filename)),
            content_type='multipart/form-data',
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)
        json_rv = json.loads(rv.data.decode('utf-8'))

        self.assertTrue(
            json_rv['files'][0]['sha256'] == sample.sha256)

        rv = self.client.post(
            url_for('api.add_av_scan'),
            data=json.dumps(json_rv),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, rv_status=202,
            value='Your files have been submitted for AV scanning')

        os.unlink(os.path.join(
            self.app.config['APP_UPLOADS_SAMPLES'],
            sample.sha256)
        )

        rv = self.client.get(
            url_for('api.get_sample', sha256=sample.sha256),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)


    def test_get_samples(self):
        rv = self.client.get(
            url_for('api.get_samples'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'items')

    def test_api_routes_list(self):
        rv = self.client.get(
            url_for('api.api_index'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'endpoints')

    def test_honey_tokens(self):
        rv = self.client.get(
            url_for('api.teapot'),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', "I'm a teapot", 418)

        rv = self.client.get(
            url_for('api.api_honeytoken'),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, 'message', 'No such user', 200)

    def test_reports(self):
        rv = self.client.get(
            url_for('api.get_reports'),
            headers=self.get_req_headers()
        )
        self.assertJSONIsNotNone(rv, 'items')

    def test_get_report(self):
        rv = self.client.get(
            url_for('api.get_report', report_id=1),
            headers=self.get_req_headers()
        )
        self.assertFalse(rv.status_code == 200)

    def test_get_sample_report(self):
        rv = self.client.get(
            url_for('api.get_sample_report', sha256='1eeb2b09a4bf6c87b273305'),
            headers=self.get_req_headers()
        )
        self.assertFalse(rv.status_code == 200)
