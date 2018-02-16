"""Test for StatsReply message."""
from pyof.v0x01.controller2switch.common import StatsType
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestStruct


class TestStatsReply(TestStruct):
    """Test for StatsReply message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/StatsReply] - size 12."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_stats_reply')
        super().set_raw_dump_object(StatsReply, xid=1,
                                    body_type=StatsType.OFPST_FLOW,
                                    flags=0x0001, body=b'')
        super().set_minimum_size(12)
