"""Flow stats message."""
from pyof.v0x04.controller2switch.multipart_reply import FlowStats
from tests.test_struct import TestStruct


class TestFlowStats(TestStruct):
    """Flow stats message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_flow_stats')
        super().set_raw_dump_object(FlowStats)
        super().set_minimum_size(56)
