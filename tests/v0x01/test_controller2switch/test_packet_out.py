import unittest

from pyof.v0x01.common import phy_port
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch import packet_out
from pyof.v0x01.foundation.exceptions import ValidationError


class TestPacketOut(unittest.TestCase):
    def setUp(self):
        self.message = packet_out.PacketOut()
        self.message.header.xid = 80
        self.message.buffer_id = 5
        self.message.in_port = phy_port.Port.OFPP_NONE
        self.message.actions_len = 0

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

    def test_valid_virtual_in_ports(self):
        """Valid virtual ports as defined in 1.0.1 spec."""
        valid = (Port.OFPP_LOCAL, Port.OFPP_CONTROLLER, Port.OFPP_NONE)
        msg = packet_out.PacketOut()
        for in_port in valid:
            msg.in_port = in_port
            self.assertTrue(msg.is_valid())

    def test_invalid_virtual_in_ports(self):
        """Invalid virtual ports as defined in 1.0.1 spec."""
        invalid = (Port.OFPP_IN_PORT, Port.OFPP_TABLE, Port.OFPP_NORMAL,
                   Port.OFPP_FLOOD, Port.OFPP_ALL)
        for in_port in invalid:
            self.message.in_port = in_port
            self.assertFalse(self.message.is_valid())
            self.assertRaises(ValidationError, self.message.validate)

    def test_valid_physical_in_ports(self):
        """Physical port limits from 1.0.0 spec."""
        max_valid = int(Port.OFPP_MAX.value) - 1
        for in_port in (1, max_valid):
            self.message.in_port = in_port
            self.assertTrue(self.message.is_valid())

    def test_invalid_physical_in_port(self):
        """Physical port limits from 1.0.0 spec."""
        max_valid = int(Port.OFPP_MAX.value) - 1
        for in_port in (-1, 0, max_valid + 1, max_valid + 2):
            self.message.in_port = in_port
            self.assertFalse(self.message.is_valid())
            self.assertRaises(ValidationError, self.message.validate)
