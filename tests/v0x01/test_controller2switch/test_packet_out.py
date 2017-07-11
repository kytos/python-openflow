"""Packet out message tests."""
from pyof.foundation.exceptions import ValidationError
from pyof.v0x01.common.action import ActionOutput, ListOfActions
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.packet_out import PacketOut
from tests.test_struct import TestMsgDumpFile


class TestPacketOut(TestMsgDumpFile):
    """Packet out message tests (also those in :class:`.TestDump`).

    Attributes:
        message (PacketOut): The message configured in :meth:`setUpClass`.
    """

    dumpfile = 'v0x01/ofpt_packet_out.dat'

    actions = ListOfActions(items=ActionOutput(port=1, max_length=0))
    data = b'\x01# \x00\x00\x01\xd2A\xc6.*@\x88\xcc\x02\x07\x07dpi'
    data += b'd:1\x04\x02\x021\x06\x02\x00x\x0c\x06dpid:1\x00\x00'
    obj = PacketOut(xid=8, buffer_id=4294967295,
                    in_port=Port.OFPP_NONE, data=data,
                    actions=actions)
    min_size = 16

    def _get_new_obj(self, port):
        return PacketOut(xid=8, buffer_id=4294967295,
                         in_port=port, data=self.data,
                         actions=self.actions)

    def test_valid_virtual_in_ports(self):
        """Valid virtual ports as defined in 1.0.1 spec."""
        valid = (Port.OFPP_LOCAL, Port.OFPP_CONTROLLER, Port.OFPP_NONE)
        for in_port in valid:
            obj = self._get_new_obj(in_port)
            self.assertTrue(obj.is_valid())

    def test_invalid_virtual_in_ports(self):
        """Invalid virtual ports as defined in 1.0.1 spec."""
        invalid = (Port.OFPP_IN_PORT, Port.OFPP_TABLE, Port.OFPP_NORMAL,
                   Port.OFPP_FLOOD, Port.OFPP_ALL)
        for in_port in invalid:
            obj = self._get_new_obj(in_port)
            self.assertFalse(obj.is_valid())
            self.assertRaises(ValidationError, obj.validate)

    def test_valid_physical_in_ports(self):
        """Physical port limits from 1.0.0 spec."""
        max_valid = int(Port.OFPP_MAX.value) - 1
        for in_port in (1, max_valid):
            obj = self._get_new_obj(in_port)
            self.assertTrue(obj.is_valid())

    def test_invalid_physical_in_port(self):
        """Physical port limits from 1.0.0 spec."""
        max_valid = int(Port.OFPP_MAX.value) - 1
        for in_port in (-1, 0, max_valid + 1, max_valid + 2):
            obj = self._get_new_obj(in_port)
            self.assertFalse(obj.is_valid())
            self.assertRaises(ValidationError, obj.validate)
