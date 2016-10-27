"""Test FlowStats message."""
import unittest

from pyof.v0x01.common import flow_match
from pyof.v0x01.controller2switch.common import FlowStats


class TestFlowStats(unittest.TestCase):
    """Test class for TestFlowStats."""

    def setUp(self):
        """Test basic setup."""
        self.message = FlowStats()
        self.message.length = 160
        self.message.table_id = 1
        self.message.match = flow_match.Match()
        self.message.duration_sec = 60
        self.message.duration_nsec = 10000
        self.message.priority = 1
        self.message.idle_timeout = 300
        self.message.hard_timeout = 6000
        self.message.cookie = 1
        self.message.packet_count = 1
        self.message.byte_count = 1
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
        """[Controller2Switch/FlowStats] - size 88."""
        self.assertEqual(self.message.get_size(), 88)

    def test_pack_unpack(self):
        """[Controller2Switch/FlowStats] - packing and unpacking."""
        pack = self.message.pack()
        unpacked = FlowStats()
        unpacked.unpack(pack)
        self.assertEqual(self.message.pack(), unpacked.pack())

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FlowStats] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/FlowStats] - unpacking."""
        # TODO
        pass
