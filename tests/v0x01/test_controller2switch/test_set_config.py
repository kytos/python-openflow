import unittest

from pyof.v0x01.controller2switch import flow_mod
from pyof.v0x01.controller2switch import set_config


class TestSetConfig(unittest.TestCase):

    def setUp(self):
        self.message = set_config.SetConfig()
        self.message.header.xid = 1
        self.message.flags = flow_mod.FlowModFlags.OFPFF_EMERG
        self.message.miss_send_len = 1024

    def test_get_size(self):
        """[Controller2Switch/SetConfig] - size 12"""
        self.assertEqual(self.message.get_size(), 12)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/SetConfig] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/SetConfig] - unpacking"""
        # TODO
        pass
