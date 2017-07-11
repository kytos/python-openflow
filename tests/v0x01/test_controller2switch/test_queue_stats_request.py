"""Test for QueueStatsRequest message."""
from pyof.v0x01.controller2switch.common import QueueStatsRequest, StatsTypes
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestMsgDumpFile


class TestQueueStatsRequest(TestMsgDumpFile):
    """Test for QueueStatsRequest message."""

    dumpfile = 'v0x01/ofpt_queue_stats_request.dat'
    obj = StatsRequest(xid=14, body_type=StatsTypes.OFPST_QUEUE,
                       flags=0,
                       body=QueueStatsRequest(port_no=80,
                                              queue_id=5))
    min_size = 12
