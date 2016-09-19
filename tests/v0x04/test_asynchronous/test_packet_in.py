"""Packet in message tests."""
from pyof.v0x04.asynchronous.packet_in import PacketIn, PacketInReason
from tests.test_struct import TestStruct


class TestPacketIn(TestStruct):
    """Packet in message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_packet_in')
        super().set_raw_dump_object(PacketIn, xid=1, buffer_id=1, total_len=1,
                                    reason=PacketInReason.OFPR_ACTION,
                                    table_id=1, cookie=1, data=b'')
        # Different from the specification, the minimum size of this class is
        # 18, not 20.
        super().set_minimum_size(34)
