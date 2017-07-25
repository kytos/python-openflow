"""Test for StatsReply message."""
from pyof.v0x01.controller2switch.common import StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestStatsReply(TestMsgDumpFile):
    """Test for StatsReply message."""

    dumpfile = 'v0x01/ofpt_stats_reply.dat'
    obj = StatsReply(xid=1, body_type=StatsTypes.OFPST_FLOW,
                     flags=0x0001, body=[])
    min_size = 12
