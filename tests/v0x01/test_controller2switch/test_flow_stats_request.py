"""Test FlowStatsRequest message."""
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.controller2switch.common import FlowStatsRequest, StatsTypes
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestStruct


class TestFlowStatsRequest(TestStruct):
    """Test class for TestFlowStatsRequest."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/FlowStatsRequest] - size 44."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_flow_stats_request')
        super().set_raw_dump_object(StatsRequest, xid=12,
                                    body_type=StatsTypes.OFPST_FLOW,
                                    flags=0, body=_get_flow_stats_request())
        super().set_minimum_size(12)


def _get_flow_stats_request():
    return FlowStatsRequest(match=_get_match(), table_id=1, out_port=80)


def _get_match():
    """Function used to return a Match instance."""
    return Match(in_port=80, dl_src='01:02:03:04:05:06',
                 dl_dst='01:02:03:04:05:06', dl_vlan=1,
                 dl_vlan_pcp=1, dl_type=1,
                 nw_tos=1, nw_proto=1,
                 nw_src='192.168.0.1', nw_dst='192.168.0.1',
                 tp_src=80, tp_dst=80)
