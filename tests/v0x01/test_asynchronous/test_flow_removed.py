import unittest

from pyof.v0x01.asynchronous import flow_removed
from pyof.v0x01.common import flow_match


class TestFlowRemoved(unittest.TestCase):
    """Test the FlowRemoved message"""

    def setUp(self):
        """Setup the TestFlowremoved Class instantiating"""
        self.message = flow_removed.FlowRemoved()
        self.message.header.xid = 1
        self.message.match = flow_match.Match()
        self.message.cookie = 0
        self.message.priority = 1
        self.message.reason = flow_removed.FlowRemovedReason.OFPRR_IDLE_TIMEOUT
        self.message.duration_sec = 4
        self.message.duration_nsec = 23
        self.message.idle_timeout = 9
        self.message.packet_count = 10
        self.message.byte_count = 4
        self.message.match.wildcards = flow_match.FlowWildCards.OFPFW_TP_DST
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

    def test_size(self):
        """[Asynchronous/FlowRemoved] - size 88"""
        self.assertEqual(self.message.get_size(), 88)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Asynchronous/FlowRemoved] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Asynchronous/FlowRemoved] - unpacking"""
        # TODO
        pass
