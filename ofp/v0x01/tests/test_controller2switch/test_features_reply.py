import unittest
import sys
import os

from ofp.v0x01.controller2switch import features_reply
from ofp.v0x01.foundation import basic_types


class TestSwitchFeatures(unittest.TestCase):

    def test_get_size(self):
        switch_features = features_reply.SwitchFeatures(
            1, 1, 1, 1, basic_types.UBInt8Array(value=0, length=3), 1, 1)
        self.assertEqual(switch_features.get_size(), 32)

    def test_pack(self):
        switch_features = features_reply.SwitchFeatures(
            1, 1, 1, 1, basic_types.UBInt8Array(value=0, length=3), 1, 1)
        switch_features.pack()

    def test_unpack(self):
        pass
