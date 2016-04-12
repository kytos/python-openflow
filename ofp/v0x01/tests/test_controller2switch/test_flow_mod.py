import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.flow_mod import FlowMod

class TestFlowMod(unittest.TestCase):
    def test_get_size(self):
        fm = FlowMod(1, 300, 6000, 1, 1, 80, 0, 1)
        self.assertEqual(fm.get_size(), 72)

    def test_pack(self):
        fm = FlowMod(1, 300, 6000, 1, 1, 80, 0, 1)
        fm.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
