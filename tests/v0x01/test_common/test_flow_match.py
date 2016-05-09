import unittest

from pyof.v0x01.common import flow_match


class TestMatch(unittest.TestCase):

    def setUp(self):
        self.message = flow_match.Match()
        self.message.wildcards = flow_match.FlowWildCards.OFPFW_IN_PORT
        self.message.in_port = 22
        self.message.dl_src = [192, 168, 0, 2]
        self.message.dl_dst = [129, 168, 0, 3]
        self.message.dl_vlan = 1
        self.message.dl_vlan_pcp = 1
        self.message.dl_type = 1
        self.message.nw_tos = 1
        self.message.nw_proto = 1
        self.message.nw_src = 10000
        self.message.nw_dst = 10000
        self.message.tp_src = 22
        self.message.tp_dst = 22

    def test_get_size(self):
        """[Common/FlowMatch] - size 40"""
        self.assertEqual(self.message.get_size(), 40)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/FlowMatch] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/FlowMatch] - unpacking"""
        # TODO
        pass
