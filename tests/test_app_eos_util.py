from unittest import TestCase
from app.eos.util import response_with_content_type, generate_checksum

class TestEOSUtil(TestCase):
    def test_generate_checksum(self):
        expected = {
            'sha1': 'b60d607b4ac8b78e457e70d6bde1472c7086e176',
            'size': 17
        }
        got = generate_checksum('generate_checksum')
        self.assertEquals(expected, got)
