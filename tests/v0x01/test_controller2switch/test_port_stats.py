"""Test for PortStats structure."""
from pyof.v0x01.controller2switch.common import PortStats, StatsType
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestStruct


class TestPortStats(TestStruct):
    """Test for PortStats structure."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/PortStats] - size 104."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_port_stats')
        super().set_raw_dump_object(StatsReply, xid=13,
                                    body_type=StatsType.OFPST_PORT,
                                    flags=0, body=_get_port_stats())
        super().set_minimum_size(12)


def _get_port_stats():
    """Function used to return a PortStats instance."""
    return PortStats(port_no=80, rx_packets=5, tx_packets=10,
                     rx_bytes=200, tx_bytes=400, rx_dropped=0,
                     tx_dropped=0, rx_errors=0, tx_errors=0,
                     rx_frame_err=0, rx_over_err=0,
                     rx_crc_err=0, collisions=0)
