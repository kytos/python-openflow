import unittest

from ofp.v0x01.controller2switch import port_mod
from ofp.v0x01.foundation import base


class TestPortMod(unittest.TestCase):

    def setUp(self):
        self.message = port_mod.PortMod()
        self.message.header.xid = 1
        self.message.port_no = 80
        self.message.hw_addr = [1 for _ in range(base.OFP_ETH_ALEN)]
        self.message.config = 1 << 2
        self.message.mask = 1 << 1
        self.message.advertise = 1
        self.message.pad = [0, 0, 0, 0]

    def test_get_size(self):
        """[Controller2Switch/PortMod] - size 32"""
        self.assertEqual(self.message.get_size(), 32)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/PortMod] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/PortMod] - unpacking"""
        # TODO
        pass
