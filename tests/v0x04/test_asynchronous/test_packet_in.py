"""Packet in message tests."""
from pyof.v0x04.asynchronous.packet_in import PacketIn, PacketInReason
from pyof.v0x04.common.flow_match import OxmTLV, Match
from tests.test_struct import TestMsgDump, TestMsgDumpFile


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


class TestPacketInDump(TestMsgDump):
    """Packet in message tests (also those in :class:`.TestDump`)."""
    obj = packetin
    dump = dump


class TestPacketInDumpFile(TestMsgDumpFile):
    """Packet in message tests (also those in :class:`.TestDump`)."""
    dumpfile = 'v0x04/ofpt_packet_in.dat'
    obj = PacketIn(xid=1, buffer_id=1, total_len=1,
                   reason=PacketInReason.OFPR_ACTION,
                   table_id=1, cookie=1, data=b'')
