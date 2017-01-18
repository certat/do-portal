import unittest
import socket
from app import utils


class UtilsTestCase(unittest.TestCase):

    def test_email_validation(self):
        self.assertTrue(utils.is_valid_email('cert-eu@ec.europa.eu'))
        self.assertFalse(utils.is_valid_email('ec.europa.eu'))

    def test_add_slashes(self):
        self.assertEqual(
            utils.addslashes('{"key": "val"}'),
            '{\\"key\\": \\"val\\"}'
        )
