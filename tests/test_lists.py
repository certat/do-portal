import os
import shutil
import random
import json
import gnupg
from flask import url_for
from tests import DOTestCase
from tests.test_gpg import FakeGPG
from app.models import User, MailmanQuery
from app.models import MailmanDomain
from unittest.mock import patch, Mock, MagicMock

testlist = 'test-' + str(random.choice(range(666)))


class ListsTestCase(DOTestCase):

    @classmethod
    def setUpClass(cls):
        gnupg.GPG = FakeGPG

    def setUp(self):
        super().setUp()
        self.currrent_user = User.create_test_user()
        self.login(self.currrent_user.email)
        self.testlistid = '{}.{}'.format(
            testlist, self.app.config['MAILMAN_DOMAIN'])

    def tearDown(self):
        self.currrent_user = None
        gpg_path = self.app.config['GPG_HOME']
        if os.path.isdir(gpg_path):
            shutil.rmtree(gpg_path)
        super().tearDown()

    def test_check_gpg(self):
        self.login(self.currrent_user.email)

    @patch.object(MailmanQuery, 'all')
    def test_get_lists(self, listmanager):
        listmanager.return_value = [
            MagicMock(
                list_id=self.testlistid,
                fqdn_listname=testlist,
                display_name=testlist,
                id=self.testlistid,
                members=[
                    MagicMock(email="alex@cert.europa.eu"),
                ],
                settings={
                    "acceptable_aliases": [],
                    "admin_immed_notify": True,
                    "admin_notify_mchanges": False,
                    "administrivia": True,
                    "advertised": True,
                    "allow_list_posts": True,
                    "anonymous_list": False,
                    "archive_policy": "public",
                    "autorespond_owner": "none",
                    "autorespond_postings": "none",
                    "autorespond_requests": "none",
                    "autoresponse_grace_period": "90d",
                    "autoresponse_owner_text": "",
                    "autoresponse_postings_text": "",
                    "autoresponse_request_text": "",
                    "collapse_alternatives": True,
                    "convert_html_to_plaintext": False,
                    "created_at": "2015-10-29T16:29:56.521055",
                    "default_member_action": "defer",
                    "default_nonmember_action": "hold",
                    "description": "aka List 1",
                    "digest_last_sent_at": None,
                    "digest_size_threshold": 30.0,
                    "display_name": "Constituents",
                    "filter_content": False,
                    "first_strip_reply_to": False,
                    "include_rfc2369_headers": True,
                    "last_post_at": None,
                    "list_name": "constituents",
                    "mail_host": "lists.cert.europa.eu",
                    "next_digest_number": 1,
                    "no_reply_address": "noreply@lists.cert.europa.eu",
                    "post_id": 1,
                    "posting_address": "constituents@lists.cert.europa.eu",
                    "posting_pipeline": "default-posting-pipeline",
                    "reply_goes_to_list": "no_munging",
                    "reply_to_address": "",
                    "scheme": "http",
                    "send_welcome_message": False,
                    "subject_prefix": "[Constituents] ",
                    "subscription_policy": "moderate",
                    "volume": 1,
                    "web_host": "lists.cert.europa.eu",
                    "welcome_message_uri": "mailman:///welcome.txt"
                }
            )]
        rv = self.client.get(
            url_for('api.get_lists'),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

    @patch.object(MailmanQuery, 'get')
    @patch.object(MailmanDomain, 'create_list')
    def new_test_create_list(self, domainmanager, listcreator):
        rv = self.client.post(
            url_for('api.add_list'),
            data=json.dumps(dict(
                name=testlist,
                description='Test list: '.format(testlist)
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

    def test_lists(self):
        nlist = 'test-' + str(random.choice(range(666)))
        nlist_id = '{}.{}'.format(nlist, self.app.config['MAILMAN_DOMAIN'])

        # create list
        rv = self.client.post(
            url_for('api.add_list'),
            data=json.dumps(dict(
                name=nlist,
                description='Test list'
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 201)

        # subscribe
        rv = self.client.put(
            url_for('api.subscribe_list', list_id=nlist_id),
            data=json.dumps(dict(emails=["test@test.com"])),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # get list
        rv = self.client.get(
            url_for('api.get_list', list_id=nlist_id),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, key='id', value=nlist_id)

        # check_gpg
        rv = self.client.get(
            url_for('api.check_gpg', list_id=nlist_id),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(
            rv, value='Test successful.')

        # unsubscribe
        rv = self.client.put(
            url_for('api.unsubscribe_list', list_id=nlist_id),
            data=json.dumps(["test@test.com"]),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        # update list
        rv = self.client.put(
            url_for('api.update_list', list_id=nlist_id),
            data=json.dumps(dict(
                name=nlist, description='test list updated',
                settings={}
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)

        rv = self.client.post(
            url_for('api.post_message'),
            data=json.dumps(dict(
                list_id=nlist_id, subject='zZz', content='ž', encrypted=True
            )),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 400)

        rv = self.client.post(
            url_for('api.post_message'),
            data=json.dumps(dict(
                list_id=nlist_id, subject='zZz', content='ž', encrypted=False
            )),
            headers=self.get_req_headers()
        )
        self.assertJSONMsg(rv, value='Email has been sent.')

        # delete list
        rv = self.client.delete(
            url_for('api.delete_list', list_id=nlist_id),
            headers=self.get_req_headers()
        )
        self.assertTrue(rv.status_code == 200)
