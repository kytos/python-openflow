"""Test for QueueStats."""
import unittest

from pyof.v0x01.controller2switch.common import QueueStats


class TestQueueStats(unittest.TestCase):
    """Test for QueueStats."""

    def setUp(self):
        """Basic Test SetUp."""
        self.message = QueueStats()
        self.message.port_no = 80
        self.message.queue_id = 5
        self.message.tx_bytes = 1
        self.message.tx_packets = 3
        self.message.tx_errors = 2

    def test_get_size(self):
        """[Controller2Switch/QueueStats] - size 32."""
        self.assertEqual(self.message.get_size(), 32)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/QueueStats] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/QueueStats] - unpacking."""
        # TODO
        pass
