"""Test  AggregateStatsRequest message."""
import unittest

from pyof.v0x01.common import flow_match, phy_port
from pyof.v0x01.controller2switch.common import AggregateStatsRequest


class TestAggregateStatsRequest(unittest.TestCase):
    """Test class for TestAggregateStatsRequest."""

    def setUp(self):
        """Test basic setup."""
        self.message = AggregateStatsRequest()
        self.message.match = flow_match.Match()
        self.message.table_id = 1
        self.message.out_port = phy_port.Port.OFPP_NONE
        self.message.match.wildcards = flow_match.FlowWildCards.OFPFW_TP_DST
        self.message.match.in_port = 80
        self.message.match.dl_src = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_dst = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_vlan = 1
        self.message.match.dl_vlan_pcp = 1
        self.message.match.dl_type = 1
        self.message.match.nw_tos = 1
        self.message.match.nw_proto = 1
        self.message.match.nw_src = [192, 168, 0, 1]
        self.message.match.nw_dst = [192, 168, 0, 1]
        self.message.match.tp_src = 80
        self.message.match.tp_dst = 80

    def test_get_size(self):
        """[Controller2Switch/AggregateStatsRequest] - size 44."""
        self.assertEqual(self.message.get_size(), 44)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/AggregateStatsRequest] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/AggregateStatsRequest] - unpacking."""
        # TODO
        pass
