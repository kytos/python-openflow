"""Packet in message tests."""
from pyof.v0x01.asynchronous.packet_in import PacketIn, PacketInReason
from tests.test_struct import TestStruct


class TestPacketIn(TestStruct):
    """Packet in message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_packet_in')
        super().set_raw_dump_object(PacketIn, xid=15, buffer_id=1, total_len=1,
                                    in_port=1,
                                    reason=PacketInReason.OFPR_ACTION)
        # Different from the specification, the minimum size of this class is
        # 18, not 20.
        super().set_minimum_size(18)
