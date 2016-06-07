import unittest

from pyof.v0x01.common import flow_match
from pyof.v0x01.controller2switch.common import FlowStatsRequest


class TestFlowStatsRequest(unittest.TestCase):

    def setUp(self):
        self.message = FlowStatsRequest()
        self.message.match = flow_match.Match()
        self.message.table_id = 1
        self.message.out_port = 80
        self.message.match.in_port = 80
        self.message.match.dl_src = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_dst = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_vlan = 1
        self.message.match.dl_vlan_pcp = 1
        self.message.match.dl_type = 1
        self.message.match.nw_tos = 1
        self.message.match.nw_proto = 1
        self.message.match.nw_src = 10000
        self.message.match.nw_dst = 10000
        self.message.match.tp_src = 80
        self.message.match.tp_dst = 80

    def test_get_size(self):
        """[Controller2Switch/FlowStatsRequest] - size 44"""
        self.assertEqual(self.message.get_size(), 44)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FlowStatsRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/FlowStatsRequest] - unpacking"""
        # TODO
        pass
