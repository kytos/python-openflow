import unittest

from ofp.v0x01.common import flow_match
from ofp.v0x01.controller2switch import aggregate_stats_request as asr


class TestAggregateStatsRequest(unittest.TestCase):
    def setUp(self):
        match = flow_match.OFPMatch(wildcards=1, in_port=22, dl_src=[],
                                    dl_dst=[], dl_vlan=1, dl_vlan_pcp=1,
                                    pad1=[0], dl_type=1, nw_tos=1, nw_proto=1,
                                    pad2=[0, 0], nw_src=10000, nw_dst=10000,
                                    tp_src=22, tp_dst=22)
        self.agg_stats_request = asr.AggregateStatsRequest(match=match,
                                                           table_id=1,
                                                           pad=0,
                                                           out_port=80)

    def test_get_size(self):
        self.assertEqual(self.agg_stats_request.get_size(), 44)

    def test_pack(self):
        self.agg_stats_request.pack()

    def test_unpack(self):
        pass
