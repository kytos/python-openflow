"""Testing v0x04 FlowRemoved message."""
from pyof.v0x04.asynchronous.flow_removed import FlowRemoved
from pyof.v0x04.common.flow_match import Match
from tests.test_struct import TestStruct


class TestFlowRemovedMsg(TestStruct):
    """FlowRemoved message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_flow_removed')
        super().set_raw_dump_object(FlowRemoved, xid=1, cookie=1, priority=1,
                                    reason=1, table_id=1, duration_sec=1,
                                    duration_nsec=2, idle_timeout=3,
                                    hard_timeout=4, packet_count=1,
                                    byte_count=1, match=Match())
        super().set_minimum_size(56)
