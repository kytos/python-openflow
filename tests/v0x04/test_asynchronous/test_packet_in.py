"""Packet in message tests."""
from unittest import TestCase

from pyof.v0x04.asynchronous.packet_in import PacketIn, PacketInReason
from pyof.v0x04.common.constants import OFP_NO_BUFFER
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from pyof.v0x04.common.header import Header
from tests.test_struct import TestStruct

OXMTLV = OxmTLV(oxm_class=32768,
                oxm_field=0,
                oxm_hasmask=0,
                oxm_value=b'\x00\x00\x00\x16')

MATCH = Match(match_type=1,
              oxm_match_fields=[OXMTLV])

PACKETIN = PacketIn(xid=0,
                    buffer_id=257,
                    total_len=81,
                    reason=1,
                    table_id=0,
                    cookie=18446744073709551615,
                    match=MATCH,
                    data=81 * b'\x00')

DUMP = b'\x04\n\x00{\x00\x00\x00\x00\x00\x00\x01\x01\x00Q\x01\x00\xff\xff'
DUMP += b'\xff\xff\xff\xff\xff\xff\x00\x01\x00\x0c\x80\x00\x00\x04\x00\x00'
DUMP += b'\x00\x16\x00\x00\x00\x00\x00\x00'
DUMP += 81 * b'\x00'


class TestPacketIn(TestCase):
    """Test PacketIn class."""

    def test_pack(self):
        """Assert pack method returns a known dump."""
        self.assertEqual(DUMP, PACKETIN.pack())

    def test_unpack(self):
        """Assert the known dump is unpacked correctly."""
        unpacked_header = Header()
        unpacked_header.unpack(DUMP[:8])
        PACKETIN.update_header_length()
        self.assertEqual(PACKETIN.header, unpacked_header)

        unpacked_packetin = PacketIn()
        unpacked_packetin.unpack(DUMP[8:])
        unpacked_packetin.header = unpacked_header
        self.assertEqual(PACKETIN, unpacked_packetin)


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
