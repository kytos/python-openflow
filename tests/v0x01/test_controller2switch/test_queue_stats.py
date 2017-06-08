"""Test for QueueStats."""
from pyof.v0x01.controller2switch.common import QueueStats, StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestStruct


class TestQueueStats(TestStruct):
    """Test for QueueStats."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/QueueStats] - size 32."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_queue_stats_reply')
        super().set_raw_dump_object(StatsReply, xid=7,
                                    body_type=StatsTypes.OFPST_QUEUE,
                                    flags=0, body=_get_queue_stats())
        super().set_minimum_size(12)


def _get_queue_stats():
    """Function used to return a QueueStats instance."""
    return QueueStats(port_no=80, queue_id=5, tx_bytes=1,
                      tx_packets=3, tx_errors=2)
