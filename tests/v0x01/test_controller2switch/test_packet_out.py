import unittest

from ofp.v0x01.common import phy_port
from ofp.v0x01.controller2switch import packet_out


class TestPacketOut(unittest.TestCase):

    def setUp(self):
        self.message = packet_out.PacketOut()
        self.message.header.xid = 80
        self.message.buffer_id = 5
        self.message.in_pot = phy_port.Port.OFPP_NONE
        self.message.actions_len = 4
        self.message.data = [0]

    def test_get_size(self):
        """[Controller2Switch/PacketOut] - size 16"""
        self.assertEqual(self.message.get_size(), 16)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/PacketOut] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/PacketOut] - unpacking"""
        # TODO
        pass
