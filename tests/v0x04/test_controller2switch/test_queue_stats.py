"""Stats queue message."""
from pyof.v0x04.controller2switch.multipart_reply import QueueStats
from tests.test_struct import TestStruct


class TestQueueStats(TestStruct):
    """Stats queue message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_queue_stats')
        super().set_raw_dump_object(QueueStats)
        super().set_minimum_size(40)
