"""Packet in message tests."""
from pyof.v0x04.asynchronous.packet_in import PacketIn, PacketInReason
from pyof.v0x04.common.constants import OFP_NO_BUFFER
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from pyof.v0x04.common.port import PortNo
from tests.test_struct import TestStruct


class TestPacketInRaw(TestStruct):
    """Test PacketIn using a dump file."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_packet_in')
        super().set_raw_dump_object(PacketIn, xid=0, buffer_id=OFP_NO_BUFFER,
                                    total_len=90,
                                    reason=PacketInReason.OFPR_ACTION,
                                    table_id=0, cookie=0x0000000000000000,
                                    match=_new_match(), data=_get_data())
        super().set_minimum_size(34)

    def test_valid_physical_in_port(self):
        """Physical port limits from 1.3.0 spec."""
        try:
            msg = self.get_raw_dump().read()
        except FileNotFoundError:
            raise self.skipTest('No raw dump file found.')
        else:
            max_valid = int(PortNo.OFPP_MAX.value) - 1
            msg = self.get_raw_object()
            if msg.in_port in (1, max_valid):
                self.assertTrue(msg.is_valid())


def _new_match():
    """Crate new Match instance."""
    oxmtlv = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                    oxm_field=OxmOfbMatchField.OFPXMT_OFB_IN_PORT,
                    oxm_hasmask=False, oxm_value=b'\x00\x00\x00\x02')
    return Match(match_type=MatchType.OFPMT_OXM,
                 oxm_match_fields=[oxmtlv])


def _get_data():
    """Return data for PacketIn object."""
    data = b'\x33\x33\x00\x00\x00\x16\x92\xfd\x3d\x2a\x06\x0c\x86\xdd\x60\x00'
    data += b'\x00\x00\x00\x24\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    data += b'\x00\x00\x00\x00\x00\x00\xff\x02\x00\x00\x00\x00\x00\x00\x00\x00'
    data += b'\x00\x00\x00\x00\x00\x16\x3a\x00\x05\x02\x00\x00\x01\x00\x8f\x00'
    data += b'\x69\x54\x00\x00\x00\x01\x04\x00\x00\x00\xff\x02\x00\x00\x00\x00'
    data += b'\x00\x00\x00\x00\x00\x01\xff\x2a\x06\x0c'
    return data
