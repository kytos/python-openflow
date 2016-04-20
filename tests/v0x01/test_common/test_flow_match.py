import unittest

from ofp.v0x01.common import flow_match


class TestOFPMatch(unittest.TestCase):

    def setUp(self):
        self.match = flow_match.OFPMatch(wildcards=1, in_port=22, dl_src=[],
                                         dl_dst=[], dl_vlan=1, dl_vlan_pcp=1,
                                         pad1=[0], dl_type=1, nw_tos=1,
                                         nw_proto=1, pad2=[0, 0], nw_src=10000,
                                         nw_dst=10000, tp_src=22, tp_dst=22)

    def test_get_size(self):
        self.assertEqual(self.match.get_size(), 40)

    def test_pack(self):
        self.match.pack()

    def test_unpack(self):
        pass
