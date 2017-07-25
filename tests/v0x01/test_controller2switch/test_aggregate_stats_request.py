"""Test  AggregateStatsRequest message."""
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.common import (
    AggregateStatsRequest, StatsTypes)
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestMsgDumpFile


class TestAggregateStatsRequest(TestMsgDumpFile):
    """Test class for TestAggregateStatsRequest."""

    dumpfile = 'v0x01/ofpt_aggregate_request.dat'

    match = Match(in_port=80, dl_src="01:02:03:04:05:06",
                  dl_dst="01:02:03:04:05:06", dl_vlan=1,
                  dl_vlan_pcp=1, dl_type=1,
                  nw_tos=1, nw_proto=1,
                  nw_src='192.168.0.1', nw_dst='192.168.0.1',
                  tp_src=80, tp_dst=80)
    request = AggregateStatsRequest(table_id=1, out_port=Port.OFPP_NONE,
                                    match=match)
    obj = StatsRequest(xid=17,
                       body_type=StatsTypes.OFPST_AGGREGATE,
                       flags=0, body=request)
    min_size = 12
