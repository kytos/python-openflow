import unittest

from ofp.v0x01.common import action
from ofp.v0x01.common import flow_match
from ofp.v0x01.foundation import base
from ofp.v0x01.controller2switch import flow_stats

class TestFlowStats(unittest.TestCase):
    def test_get_size(self):
        match = flow_match.OFPMatch(
            wildcards=1, in_port=22, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=22, tp_dst=22)
        action_header = action.ActionHeader(1, 40, [1, 1, 1, 1])
        flow_stats_message = flow_stats.FlowStats(length=160, table_id=1,
            pad=0, match=match, duration_sec=60, duration_nsec=10000,
            priority=1, idle_timeout=300, hard_timeout=6000,
            pad2=[10, 10, 10, 10, 10, 10], cookie=1, packet_count=1,
            byte_count=1, actions=action_header)
        self.assertEqual(flow_stats_message.get_size(), 88)

    def test_pack(self):
        match = flow_match.OFPMatch(
            wildcards=1, in_port=22, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=22, tp_dst=22)
        action_header = action.ActionHeader(1, 40, [1, 1, 1, 1])
        flow_stats_message = flow_stats.FlowStats(length=160, table_id=1,
            pad=0, match=match, duration_sec=60, duration_nsec=10000,
            priority=1, idle_timeout=300, hard_timeout=6000,
            pad2=[10, 10, 10, 10, 10, 10], cookie=1, packet_count=1,
            byte_count=1, actions=action_header)
        flow_stats_message.pack()

    def test_unpack(self):
        pass
