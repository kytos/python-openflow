import unittest

from ofp.v0x01.common import flow_match
from ofp.v0x01.controller2switch import flow_stats_request


class TestFlowStatsRequest(unittest.TestCase):
    def setUp(self):
        match = flow_match.OFPMatch(wildcards=1, in_port=22, dl_src=[],
                                    dl_dst=[], dl_vlan=1, dl_vlan_pcp=1,
                                    pad1=[0], dl_type=1, nw_tos=1, nw_proto=1,
                                    pad2=[0, 0], nw_src=10000, nw_dst=10000,
                                    tp_src=22, tp_dst=22)
        self.flow_stats_req = flow_stats_request.FlowStatsRequest(match=match,
                                                                  table_id=1,
                                                                  pad=0,
                                                                  out_port=80)

    def test_get_size(self):
        self.assertEqual(self.flow_stats_req.get_size(), 44)

    def test_pack(self):
        self.flow_stats_req.pack()

    def test_unpack(self):
        pass
