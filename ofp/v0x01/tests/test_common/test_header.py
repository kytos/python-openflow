import unittest
import sys
import os

from ofp.v0x01.common import header


class TestHeader(unittest.TestCase):

    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 40, 1)
        self.assertEqual(ofp_header.get_size(), 8)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 40, 1)
        ofp_header.pack()

    def test_unpack(self):
        pass
