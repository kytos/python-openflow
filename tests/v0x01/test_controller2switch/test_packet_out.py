"""Packet out message tests."""
from pyof.foundation.exceptions import ValidationError
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.packet_out import PacketOut
from tests.test_struct import TestStruct


class TestPacketOut(TestStruct):
    """Packet out message tests (also those in :class:`.TestDump`).

    Attributes:
        message (PacketOut): The message configured in :meth:`setUpClass`.
    """

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_packet_out')
        super().set_raw_dump_object(PacketOut, xid=80, buffer_id=5,
                                    in_port=Port.OFPP_NONE)
        super().set_minimum_size(16)

    def setUp(self):
        """Run before every test."""
        self.message = self.get_raw_object()

    def test_valid_virtual_in_ports(self):
        """Valid virtual ports as defined in 1.0.1 spec."""
        valid = (Port.OFPP_LOCAL, Port.OFPP_CONTROLLER, Port.OFPP_NONE)
        for in_port in valid:
            self.message.in_port = in_port
            self.assertTrue(self.message.is_valid())

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

    def test_pack(self):
        """Skip pack test for now."""
        self.skipTest('Need to recover dump contents.')

    def test_unpack(self):
        """Skip unpack test for now."""
        self.skipTest('Need to recover dump contents.')
