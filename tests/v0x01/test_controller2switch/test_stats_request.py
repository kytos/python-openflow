"""Test for StatsRequest message."""
from pyof.v0x01.controller2switch.common import StatsTypes
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestMsgDumpFile


class TestStatsRequest(TestMsgDumpFile):
    """Test for StatsRequest message."""

    dumpfile = 'v0x01/ofpt_stats_request.dat'
    obj = StatsRequest(xid=1, body_type=StatsTypes.OFPST_FLOW,
                       flags=1, body=[])
    min_size = 12
