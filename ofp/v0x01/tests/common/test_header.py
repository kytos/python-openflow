import unittest

from common.header import OFPHeader

class TestHeader(unittest.TestCase):
    def test_get_size(self):
        header = OFPHeader()
        self.assertEqual(header.get_size(), 8)
