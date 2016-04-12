import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.features_reply import SwitchFeatures
from foundation.basic_types import UBInt8Array

class TestSwitchFeatures(unittest.TestCase):
    def test_get_size(self):
        switch_features = SwitchFeatures(
            1, 1, 1, 1, UBInt8Array(value=0, length=3), 1, 1)
        self.assertEqual(switch_features.get_size(), 32)

    def test_pack(self):
        switch_features = SwitchFeatures(
            1, 1, 1, 1, UBInt8Array(value=0, length=3), 1, 1)
        switch_features.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
