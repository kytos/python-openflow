"""Test for AggregateStatsReply message."""
from pyof.v0x01.controller2switch.common import AggregateStatsReply, StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestAggregateStatsReply(TestMsgDumpFile):
    """Test for AggregateStatsReply message."""

    dumpfile = 'v0x01/ofpt_aggregate_stats_reply.dat'
    aggregate_stats_reply = AggregateStatsReply(packet_count=5,
                                                byte_count=1, flow_count=8)
    obj = StatsReply(xid=17,
                     body_type=StatsTypes.OFPST_AGGREGATE,
                     flags=0, body=aggregate_stats_reply)
    min_size = 12
