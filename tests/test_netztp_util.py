from unittest import TestCase
from netztp import create_app
from netztp.util import response_with_content_type, generate_checksum

from config import TestConfig

class TestUtil(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_response_with_content_type(self):
        expected = {'data': b'expected', 'content_type': 'text/plain'}
        got = response_with_content_type(expected['data'], expected['content_type'])
        self.assertEqual(got.data, expected['data'])
        self.assertEqual(got.content_type, expected['content_type'])

    def test_generate_checksum(self):
        expected = {
            'sha1': 'b60d607b4ac8b78e457e70d6bde1472c7086e176',
            'size': 17
        }
        got = generate_checksum('generate_checksum')
        self.assertEquals(expected, got)
