"""Testing FlowRemoved message."""
from pyof.foundation.basic_types import HWAddress, IPAddress
from pyof.v0x01.asynchronous.flow_removed import FlowRemoved, FlowRemovedReason
from pyof.v0x01.common.flow_match import Match
from tests.test_struct import TestStruct


class TestFlowRemoved(TestStruct):
    """Test the FlowRemoved message."""

    @classmethod
    def setUpClass(cls):
        """Setup TestStruct."""
        reason = FlowRemovedReason.OFPRR_IDLE_TIMEOUT
        match = Match(in_port=80, dl_vlan=1, dl_vlan_pcp=1, dl_type=1,
                      nw_tos=1, nw_proto=1, tp_src=80, tp_dst=80,
                      dl_src=HWAddress('00:00:00:00:00:00'),
                      dl_dst=HWAddress('00:00:00:00:00:00'),
                      nw_src=IPAddress('192.168.0.1'),
                      nw_dst=IPAddress('192.168.0.2'))

        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_flow_removed')
        super().set_raw_dump_object(FlowRemoved, xid=12,
                                    match=match, cookie=0, priority=1,
                                    reason=reason, duration_sec=4,
                                    duration_nsec=23, idle_timeout=9,
                                    packet_count=10, byte_count=4)
        super().set_minimum_size(88)
