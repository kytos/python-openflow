import unittest

from ofp.v0x01.controller2switch import features_reply

class TestSwitchFeatures(unittest.TestCase):

    def test_get_size(self):
        switch_features = features_reply.SwitchFeatures(1, 1, 1, 1, [0, 0, 0],
                                                        1, 1)
        self.assertEqual(switch_features.get_size(), 32)

    def test_pack(self):
        switch_features = features_reply.SwitchFeatures(1, 1, 1, 1, [0, 0, 0],
                                                        1, 1)
        switch_features.pack()

    def test_unpack(self):
        pass
