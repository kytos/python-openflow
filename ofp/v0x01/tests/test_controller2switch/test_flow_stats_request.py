import unittest
import sys
import os

# OFP Modules to be tested
sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import flow_match
from controller2switch import flow_stats_request

class TestFlowStatsRequest(unittest.TestCase):
    def test_get_size(self):
        flow_stats_request_message = flow_stats_request.FlowStatsRequest(
            match=flow_match.OFPMatch(), table_id=1, pad=0, out_port=80)
        self.assertEqual(flow_stats_request_message.get_size(), 44)

    def test_pack(self):
        flow_stats_request_message = flow_stats_request.FlowStatsRequest(
            match=flow_match.OFPMatch(), table_id=1, pad=0, out_port=80)
        flow_stats_request_message.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
