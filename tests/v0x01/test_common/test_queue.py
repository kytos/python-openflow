"""Testing Queue structure."""
import unittest

from pyof.v0x01.common import queue


class TestQueuePropHeader(unittest.TestCase):
    """Test QueuePropHeader."""

    def setUp(self):
        """Basic setup for test."""
        self.message = queue.QueuePropHeader()
        self.message.property = queue.QueueProperties.OFPQT_MIN_RATE
        self.message.len = 12

    def test_get_size(self):
        """[Common/QueuePropHeader] - size 8."""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/QueuePropHeader] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/QueuePropHeader] - unpacking."""
        # TODO
        pass


class TestPacketQueue(unittest.TestCase):
    """TestPacketQueue."""

    def setUp(self):
        """Basic setup for test."""
        self.message = queue.PacketQueue()
        self.message.queue_id = 1
        self.message.length = 8

    def test_get_size(self):
        """[Common/PacketQueue] - size 8."""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/PacketQueue] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PacketQueue] - unpacking."""
        # TODO
        pass


class TestQueuePropMinRate(unittest.TestCase):
    """Test QueuePropMinRate."""

    def setUp(self):
        """Basic setup for test."""
        self.message = queue.QueuePropMinRate()
        self.message.rate = 1000

    def test_get_size(self):
        """[Common/PropMinRate] - size 16."""
        self.assertEqual(self.message.get_size(), 16)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/PropMinRate] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PropMinRate] - unpacking."""
        # TODO
        pass
