"""Packet in message tests."""
from unittest import TestCase

from pyof.v0x04.asynchronous.packet_in import PacketIn, PacketInReason
from pyof.v0x04.common.flow_match import Match, OxmTLV
from pyof.v0x04.common.header import Header
from tests.test_struct import TestStruct

oxmtlv = OxmTLV(oxm_class=32768,
                oxm_field=0,
                oxm_hasmask=0,
                oxm_value=b'\x00\x00\x00\x16')

match = Match(match_type=1,
              oxm_match_fields=[oxmtlv])

packetin = PacketIn(xid=0,
                    buffer_id=257,
                    total_len=81,
                    reason=1,
                    table_id=0,
                    cookie=18446744073709551615,
                    match=match,
                    data=81 * b'\x00')

dump = b'\x04\n\x00{\x00\x00\x00\x00\x00\x00\x01\x01\x00Q\x01\x00\xff\xff'
dump += b'\xff\xff\xff\xff\xff\xff\x00\x01\x00\x0c\x80\x00\x00\x04\x00\x00'
dump += b'\x00\x16\x00\x00\x00\x00\x00\x00'
dump += 81 * b'\x00'


class TestPacketIn(TestCase):
    """Test PacketIn class."""

    def test_pack(self):
        """Assert pack method returns a known dump."""
        self.assertEqual(dump, packetin.pack())

    def test_unpack(self):
        """Assert the known dump is unpacked correctly."""
        unpacked_header = Header()
        unpacked_header.unpack(dump[:8])
        packetin.update_header_length()
        self.assertEqual(packetin.header, unpacked_header)

        unpacked_packetin = PacketIn()
        unpacked_packetin.unpack(dump[8:])
        unpacked_packetin.header = unpacked_header
        self.assertEqual(packetin, unpacked_packetin)


class TestPacketInRaw(TestStruct):
    """Test PacketIn using a dump file."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_packet_in')
        super().set_raw_dump_object(PacketIn, xid=1, buffer_id=1, total_len=1,
                                    reason=PacketInReason.OFPR_ACTION,
                                    table_id=1, cookie=1, data=b'')
        super().set_minimum_size(34)
