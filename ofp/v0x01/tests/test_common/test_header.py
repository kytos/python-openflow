import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common.header import OFPHeader
from common.header import OFPType

class TestHeader(unittest.TestCase):
    def test_get_size(self):
        header = OFPHeader(1, 40, 1)
        self.assertEqual(header.get_size(), 8)

    def test_pack(self):
        header = OFPHeader(1, 40, 1);
        header.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
