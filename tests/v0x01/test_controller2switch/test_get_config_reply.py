import unittest

from pyof.v0x01.controller2switch import flow_mod
from pyof.v0x01.controller2switch import get_config_reply


class TestGetConfigReply(unittest.TestCase):

    def setUp(self):
        self.message = get_config_reply.GetConfigReply()
        self.message.header.xid = 1
        self.message.flags = flow_mod.FlowModFlags.OFPFF_EMERG
        self.message.miss_send_len = 1024

    def test_get_size(self):
        """[Controller2Switch/GetConfigReply] - size 12"""
        self.assertEqual(self.message.get_size(), 12)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/GetConfigReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/GetConfigReply] - unpacking"""
        # TODO
        pass
