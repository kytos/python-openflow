"""Test for PortStatsRequest."""
from pyof.v0x01.controller2switch.common import PortStatsRequest, StatsTypes
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestMsgDumpFile


class TestPortStatsRequest(TestMsgDumpFile):
    """Test for PortStatsRequest."""

    dumpfile = 'v0x01/ofpt_port_stats_request.dat'
    obj = StatsRequest(xid=17,
                       body_type=StatsTypes.OFPST_PORT,
                       flags=0, body=PortStatsRequest(port_no=80))
    min_size = 12
