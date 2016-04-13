import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common.header import OFPHeader
from controller2switch.stats_request import StatsRequest

class TestStatsRequest(unittest.TestCase):
    def test_get_size(self):
        sr = StatsRequest(OFPHeader(), 3, 1)
        self.assertEqual(sr.get_size(), 12)

    def test_pack(self):
        sr = StatsRequest(OFPHeader(), 3, 1)
        sr.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
