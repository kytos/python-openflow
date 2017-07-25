"""Test for PortStats structure."""
from pyof.v0x01.controller2switch.common import PortStats, StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestPortStats(TestMsgDumpFile):
    """Test for PortStats structure."""

    dumpfile = 'v0x01/ofpt_port_stats.dat'

    port_stats = PortStats(port_no=80, rx_packets=5, tx_packets=10,
                           rx_bytes=200, tx_bytes=400, rx_dropped=0,
                           tx_dropped=0, rx_errors=0, tx_errors=0,
                           rx_frame_err=0, rx_over_err=0,
                           rx_crc_err=0, collisions=0)
    obj = StatsReply(xid=13,
                     body_type=StatsTypes.OFPST_PORT,
                     flags=0, body=port_stats)
    min_size = 12
