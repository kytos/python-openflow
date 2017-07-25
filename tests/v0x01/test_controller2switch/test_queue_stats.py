"""Test for QueueStats."""
from pyof.v0x01.controller2switch.common import QueueStats, StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestQueueStats(TestMsgDumpFile):
    """Test for QueueStats."""

    dumpfile = 'v0x01/ofpt_queue_stats_reply.dat'

    queue = QueueStats(port_no=80, queue_id=5, tx_bytes=1,
                       tx_packets=3, tx_errors=2)
    obj = StatsReply(xid=7, body_type=StatsTypes.OFPST_QUEUE,
                     flags=0, body=queue)
    min_size = 12
