import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import flow_match
from foundation.base import OFP_ETH_ALEN
from foundation.basic_types import UBInt8Array


class TestOFPMatch(unittest.TestCase):
    def test_get_size(self):
        match = flow_match.OFPMatch(
            wildcards=1, in_port=22, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=22, tp_dst=22)
        self.assertEqual(match.get_size(), 40)

    def test_pack(self):
        match = flow_match.OFPMatch(
            wildcards=1, in_port=22, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=22, tp_dst=22)
        match.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
