import unittest

from ofp.v0x01.asynchronous import flow_removed
from ofp.v0x01.common import flow_match


class TestFlowRemoved(unittest.TestCase):
    """Test the FlowRemoved message"""

    def setUp(self):
        """Setup the TestFlowremoved Class instantiating"""
        match = flow_match.OFPMatch(
            wildcards=1, in_port=80, dl_src=[1, 2, 3, 4, 5, 6],
            dl_dst=[1, 2, 3, 4, 5, 6], dl_vlan=1, dl_vlan_pcp=1, pad1=[0],
            dl_type=1, nw_tos=1, nw_proto=1, pad2=[0, 0], nw_src=10000,
            nw_dst=10000, tp_src=80, tp_dst=80)
        self.message = flow_removed.FlowRemoved(xid=1, match=match, cookie=0,
                                                priority=1,
                                                reason=flow_removed.FlowRemovedReason.OFPRR_IDLE_TIMEOUT,
                                                pad=[1], duration_sec=4,
                                                duration_nsec=23,
                                                idle_timeout=9, pad2=[1, 2],
                                                packet_count=10, byte_count=4)

    def test_size(self):
        """Test the size of the message"""
        self.assertEqual(self.message.get_size(), 88)

    def test_pack(self):
        """Test the pack method for the flow_removed"""
        packet_message = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packet_message)

    def test_unpack(self):
        """Test FlowRemoved message unpacking.
        Should read a raw binary datapack, get the first 8 bytes and
        then unpack it as a FlowRemoved object."""
        # TODO
        # self.assertEqual(unpacked_header, self.header)
        pass
