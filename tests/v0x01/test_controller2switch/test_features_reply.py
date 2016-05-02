import unittest

from ofp.v0x01.common import action
from ofp.v0x01.controller2switch import features_reply


class TestSwitchFeatures(unittest.TestCase):

    def setUp(self):
        self.message = features_reply.SwitchFeatures()
        self.message.header.xid = 1
        self.message.datapath_id = 1
        self.message.n_buffers = 1
        self.message.n_tables = 1
        self.message.pad = [0, 0, 0]
        self.message.capabilities = features_reply.Capabilities.OFPC_TABLE_STATS
        self.message.actions = action.ActionType.OFPAT_SET_DL_SRC
        self.message.ports = []

    def test_get_size(self):
        """[Controller2Switch/FeaturesReply] - size 32"""
        self.assertEqual(self.message.get_size(), 32)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FeaturesReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/FeaturesReply] - unpacking"""
        # TODO
        pass
