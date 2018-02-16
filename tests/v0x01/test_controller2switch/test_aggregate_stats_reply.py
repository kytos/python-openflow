"""Test for AggregateStatsReply message."""
from pyof.v0x01.controller2switch.common import AggregateStatsReply, StatsType
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestStruct


class TestAggregateStatsReply(TestStruct):
    """Test for AggregateStatsReply message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/AggregateStatsReply] - size 24."""
        aggregate_stats_reply = AggregateStatsReply(packet_count=5,
                                                    byte_count=1, flow_count=8)
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_aggregate_stats_reply')
        super().set_raw_dump_object(StatsReply, xid=17,
                                    body_type=StatsType.OFPST_AGGREGATE,
                                    flags=0, body=aggregate_stats_reply)
        super().set_minimum_size(12)
