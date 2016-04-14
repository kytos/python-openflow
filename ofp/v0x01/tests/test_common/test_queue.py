import unittest

from ofp.v0x01.common import queue

class TestQueuePropHeader(unittest.TestCase):

    def test_get_size(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        self.assertEqual(queue_prop_header.get_size(), 8)

    def test_pack(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        queue_prop_header.pack()

    def test_unpack(self):
        pass

class TestPacketQueue(unittest.TestCase):

    def test_get_size(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        packet_queue = queue.PacketQueue(queue_id=1, len=8, pad=[0, 0],
                                         properties=queue_prop_header)
        self.assertEqual(packet_queue.get_size(), 8)

    def test_pack(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        packet_queue = queue.PacketQueue(queue_id=1, len=8, pad=[0, 0],
                                         properties=queue_prop_header)
        packet_queue.pack()

    def test_unpack(self):
        pass

class TestQueuePropMinRate(unittest.TestCase):

    def test_get_size(self):
        queue_prop_min_rate = queue.QueuePropMinRate(1000, 100000,
                                                     [0, 0, 0, 0, 0, 0])
        self.assertEqual(queue_prop_min_rate.get_size(), 16)

    def test_pack(self):
        queue_prop_min_rate = queue.QueuePropMinRate(1000, 100000,
                                                     [0, 0, 0, 0, 0, 0])
        queue_prop_min_rate.pack()

    def test_unpack(self):
        pass
