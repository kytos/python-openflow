import unittest

from ofp.v0x01.controller2switch import port_stats

class PortStats(unittest.TestCase):
    def test_get_size(self):
        port_stats_message = \
            port_stats.PortStats(port_no=80, pad=[0, 0, 0, 0, 0, 0],
                                 rx_packets=5, tx_packets=10, rx_bytes=200,
                                 tx_bytes=400, rx_dropped=0, tx_dropped=0,
                                 rx_errors=0, tx_errors=0, rx_frame_err=0,
                                 rx_over_err=0, rx_crc_err=0, collisions=0)
        self.assertEqual(port_stats_message.get_size(), 104)

    def test_pack(self):
        port_stats_message = \
            port_stats.PortStats(port_no=80, pad=[0, 0, 0, 0, 0, 0],
                                 rx_packets=5, tx_packets=10, rx_bytes=200,
                                 tx_bytes=400, rx_dropped=0, tx_dropped=0,
                                 rx_errors=0, tx_errors=0, rx_frame_err=0,
                                 rx_over_err=0, rx_crc_err=0, collisions=0)
        port_stats_message.pack()

    def test_unpack(self):
        pass
