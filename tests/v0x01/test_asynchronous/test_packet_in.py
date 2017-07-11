"""Packet in message tests."""
from pyof.v0x01.asynchronous.packet_in import PacketIn, PacketInReason
from tests.test_struct import TestMsgDumpFile


class TestPacketIn(TestMsgDumpFile):
    """Packet in message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_packet_in.dat'
    obj = PacketIn(xid=15, buffer_id=1, total_len=1,
                   in_port=1,
                   reason=PacketInReason.OFPR_ACTION)

    # Different from the specification, the minimum size of this class is
    # 18, not 20.
    min_size = 18
