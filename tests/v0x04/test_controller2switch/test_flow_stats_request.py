"""Flow stats request message."""
from pyof.v0x04.controller2switch.multipart_request import FlowStatsRequest
from tests.test_struct import TestStruct


class TestFlowStatsRequest(TestStruct):
    """Flow stats request message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_flow_stats_request')
        super().set_raw_dump_object(FlowStatsRequest)
        super().set_minimum_size(40)
