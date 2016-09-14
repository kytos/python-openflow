"""Test for PortStats structure."""
import unittest

from pyof.v0x01.controller2switch.common import PortStats


class TestPortStats(unittest.TestCase):
    """Test for PortStats structure."""

    def setUp(self):
        """Basic test Setup."""
        self.message = PortStats()
        self.message.port_no = 80
        self.message.rx_packets = 5
        self.message.tx_packets = 10
        self.message.rx_bytes = 200
        self.message.tx_bytes = 400
        self.message.rx_dropped = 0
        self.message.tx_dropped = 0
        self.message.rx_errors = 0
        self.message.tx_errors = 0
        self.message.rx_frame_err = 0
        self.message.rx_over_err = 0
        self.message.rx_crc_err = 0
        self.message.collisions = 0

    def test_get_size(self):
        """[Controller2Switch/PortStats] - size 104."""
        self.assertEqual(self.message.get_size(), 104)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/PortStats] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/PortStats] - unpacking."""
        # TODO
        pass
