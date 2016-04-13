import unittest
import sys
import os

from ofp.v0x01.common.header import OFPHeader
from ofp.v0x01.controller2switch.stats_request import StatsRequest

class TestStatsRequest(unittest.TestCase):
    def test_get_size(self):
        sr = StatsRequest(OFPHeader(), 3, 1)
        self.assertEqual(sr.get_size(), 12)

    def test_pack(self):
        sr = StatsRequest(OFPHeader(), 3, 1)
        sr.pack()

    def test_unpack(self):
        pass
