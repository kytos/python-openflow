import unittest

from ofp.v0x01.controller2switch import features_reply


class TestSwitchFeatures(unittest.TestCase):

    def setUp(self):
        self.switch_features = features_reply.SwitchFeatures(xid=1,
                                                             datapath_id=1,
                                                             n_buffers=1,
                                                             n_tables=1,
                                                             pad=[0, 0, 0],
                                                             capabilities=1,
                                                             actions=5,
                                                             ports=[])

    def test_get_size(self):
        self.assertEqual(self.switch_features.get_size(), 32)

    def test_pack(self):
        self.switch_features.pack()

    def test_unpack(self):
        pass
