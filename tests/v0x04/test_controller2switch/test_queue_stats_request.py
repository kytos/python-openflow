"""Queue Stat Request message."""
from pyof.v0x04.controller2switch.multipart_request import QueueStatsRequest
from tests.test_struct import TestStruct


class TestQueueStatsRequest(TestStruct):
    """Queue Stat Request message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_queue_stats_request')
        super().set_raw_dump_object(QueueStatsRequest)
        super().set_minimum_size(8)
