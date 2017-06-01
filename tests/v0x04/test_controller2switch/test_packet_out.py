"""Packet out message tests."""
import logging

from pyof.foundation.exceptions import ValidationError
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.packet_out import PacketOut
from tests.test_struct import TestStruct

log = logging.getLogger()
NO_RAW = 'No raw dump file found.'


class TestPacketOut(TestStruct):
    """Packet out message tests (also those in :class:`.TestDump`).

    Attributes:
        message (PacketOut): The message configured in :meth:`setUpClass`.
    """

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_packet_out')
        super().set_raw_dump_object(PacketOut, xid=80, buffer_id=5,
                                    in_port=PortNo.OFPP_ANY)
        super().set_minimum_size(24)

    def test_valid_virtual_in_ports(self):
        """Valid virtual ports as defined in 1.3.0 spec."""
        try:
            msg = self.get_raw_dump().read()
        except FileNotFoundError:
            raise self.skipTest(NO_RAW)
        else:
            valid = (PortNo.OFPP_LOCAL, PortNo.OFPP_CONTROLLER,
                     PortNo.OFPP_ANY)
            msg = self.get_raw_object()
            for in_port in valid:
                msg.in_port = in_port
                self.assertTrue(msg.is_valid())

    def test_invalid_virtual_in_ports(self):
        """Invalid virtual ports as defined in 1.3.0 spec."""
        try:
            msg = self.get_raw_dump().read()
        except FileNotFoundError:
            raise self.skipTest(NO_RAW)
        else:
            invalid = (PortNo.OFPP_IN_PORT, PortNo.OFPP_TABLE,
                       PortNo.OFPP_NORMAL, PortNo.OFPP_FLOOD, PortNo.OFPP_ALL)
            msg = self.get_raw_object()
            for in_port in invalid:
                msg.in_port = in_port
                self.assertFalse(msg.is_valid())
                self.assertRaises(ValidationError, msg.validate)

    def test_valid_physical_in_ports(self):
        """Physical port limits from 1.3.0 spec."""
        try:
            msg = self.get_raw_dump().read()
        except FileNotFoundError:
            raise self.skipTest(NO_RAW)
        else:
            max_valid = int(PortNo.OFPP_MAX.value) - 1
            msg = self.get_raw_object()
            for in_port in (1, max_valid):
                msg.in_port = in_port
                self.assertTrue(msg.is_valid())

    def test_invalid_physical_in_port(self):
        """Physical port limits from 1.3.0 spec."""
        try:
            msg = self.get_raw_dump().read()
        except FileNotFoundError:
            raise self.skipTest(NO_RAW)
        else:
            max_valid = int(PortNo.OFPP_MAX.value) - 1
            msg = self.get_raw_object()
            for in_port in (-1, 0, max_valid + 1, max_valid + 2):
                msg.in_port = in_port
                self.assertFalse(msg.is_valid())
                self.assertRaises(ValidationError, msg.validate)
