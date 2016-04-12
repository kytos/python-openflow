import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.get_config_reply import SwitchConfig

class TestSwitchConfig(unittest.TestCase):
    def test_get_size(self):
        gcr = SwitchConfig(xid=1, flags=1)
        self.assertEqual(gcr.get_size(), 16)

    def test_pack(self):
        gcr = SwitchConfig(xid=1, flags=1)
        gcr.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
