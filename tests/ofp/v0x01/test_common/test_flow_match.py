import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import flow_match

class TestOFPMatch(unittest.TestCase):
    def test_get_size(self):
        match = flow_match.OFPMatch()
        self.assertEqual(match.get_size(), 40)

    def test_pack(self):
        match = flow_match.OFPMatch()
        match.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
