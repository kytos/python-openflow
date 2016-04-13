import unittest
import sys
import os

# OFP Modules to be tested
sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import action
from common import flow_match
from foundation import base
from foundation import basic_types
from controller2switch import flow_stats

class TestFlowStats(unittest.TestCase):
    def test_get_size(self):
        match = flow_match.OFPMatch(
            1, 22, basic_types.UBInt8Array(value=123456,
            length=base.OFP_ETH_ALEN),
            basic_types.UBInt8Array(value=123456, length=base.OFP_ETH_ALEN),
            1, 1, basic_types.UBInt8Array(value=0, length=1), 1, 1, 1,
            basic_types.UBInt8Array(value=0, length=2), 10000, 10000, 22, 22)
        action_header = action.ActionHeader(
            1, 40, basic_types.UBInt8Array(value=255, length=4))
        flow_stats_message = flow_stats.FlowStats(length=160, table_id=1,
            pad=0, match=match, duration_sec=60, duration_nsec=10000, priority=1,
            idle_timeout=300, hard_timeout=6000,
            pad2=basic_types.UBInt8Array(value=0, length=6),
            cookie=1, packet_count=1, byte_count=1, actions=action_header)
        self.assertEqual(flow_stats_message.get_size(), 88)

    def test_pack(self):
        match = flow_match.OFPMatch(
            1, 22, basic_types.UBInt8Array(value=123456,
            length=base.OFP_ETH_ALEN),
            basic_types.UBInt8Array(value=123456, length=base.OFP_ETH_ALEN),
            1, 1, basic_types.UBInt8Array(value=0, length=1), 1, 1, 1,
            basic_types.UBInt8Array(value=0, length=2), 10000, 10000, 22, 22)
        action_header = action.ActionHeader(
            1, 40, basic_types.UBInt8Array(value=255, length=4))
        flow_stats_message = flow_stats.FlowStats(length=160, table_id=1,
            pad=0, match=match, duration_sec=60, duration_nsec=10000, priority=1,
            idle_timeout=300, hard_timeout=6000,
            pad2=basic_types.UBInt8Array(value=0, length=6),
            cookie=1, packet_count=1, byte_count=1, actions=action_header)
        flow_stats_message.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
