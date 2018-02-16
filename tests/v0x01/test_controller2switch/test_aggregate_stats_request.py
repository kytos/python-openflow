"""Test  AggregateStatsRequest message."""
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.common import (
    AggregateStatsRequest, StatsType)
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestStruct


class TestAggregateStatsRequest(TestStruct):
    """Test class for TestAggregateStatsRequest."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/AggregateStatsRequest] - size 44."""
        request = AggregateStatsRequest(table_id=1, out_port=Port.OFPP_NONE,
                                        match=_get_match())

        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_aggregate_request')
        super().set_raw_dump_object(StatsRequest, xid=17,
                                    body_type=StatsType.OFPST_AGGREGATE,
                                    flags=0, body=request)
        super().set_minimum_size(12)


def _get_match():
    """Function used to built Match instance used by AggregateStatsRequest."""
    return Match(in_port=80, dl_src="01:02:03:04:05:06",
                 dl_dst="01:02:03:04:05:06", dl_vlan=1,
                 dl_vlan_pcp=1, dl_type=1,
                 nw_tos=1, nw_proto=1,
                 nw_src='192.168.0.1', nw_dst='192.168.0.1',
                 tp_src=80, tp_dst=80)
