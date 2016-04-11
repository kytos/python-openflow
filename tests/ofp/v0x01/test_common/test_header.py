import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common.header import OFPHeader
from common.header import OFPType

class TestHeader(unittest.TestCase):
    def test_get_size(self):
        header = OFPHeader()
        self.assertEqual(header.get_size(), 8)

    def test_pack(self):
        header = OFPHeader();
        header.pack()

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
