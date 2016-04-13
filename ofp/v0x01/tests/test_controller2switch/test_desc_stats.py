import unittest
import sys
import os

# OFP Modules to be tested
sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch import desc_stats

class TestDescStats(unittest.TestCase):
    def test_get_size(self):
        pass

    def test_pack(self):
        pass

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
