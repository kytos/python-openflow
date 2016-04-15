import unittest

from ofp.v0x01.common import action
from ofp.v0x01.common import flow_match
from ofp.v0x01.common import header
from ofp.v0x01.controller2switch import flow_mod

class TestFlowMod(unittest.TestCase):

    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 88, 1)
        match = flow_match.OFPMatch(
            wildcards=1, in_port=80, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=80, tp_dst=80)
        action_header = action.ActionHeader(1, 40, [15, 15, 15, 15])
        flow_mod_message = flow_mod.FlowMod(command=1, header=ofp_header,
                                            match=match, cookie=0,
                                            idle_timeout=300, hard_timeout=6000,
                                            priority=1, buffer_id=1,
                                            out_port=80, flags=0,
                                            actions=action_header)
        self.assertEqual(flow_mod_message.get_size(), 80)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 88, 1)
        match = flow_match.OFPMatch(
            wildcards=1, in_port=80, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=80, tp_dst=80)
        action_header = action.ActionHeader(1, 40, [15, 15, 15, 15])
        flow_mod_message = flow_mod.FlowMod(command=1, header=ofp_header,
                                            match=match, cookie=0,
                                            idle_timeout=300, hard_timeout=6000,
                                            priority=1, buffer_id=1,
                                            out_port=80, flags=0,
                                            actions=action_header)
        flow_mod_message.pack()

    def test_unpack(self):
        pass
