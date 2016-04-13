import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import queue
from foundation import basic_types


class TestPacketQueue(unittest.TestCase):

    def test_get_size(self):
        packet_queue = queue.PacketQueue(1, 8, [0, 0])
        self.assertEqual(packet_queue.get_size(), 8)

    def test_pack(self):
        packet_queue = queue.PacketQueue(1, 8, [0, 0])
        packet_queue.pack()

    def test_unpack(self):
        pass


class TestQueuePropHeader(unittest.TestCase):

    def test_get_size(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        self.assertEqual(queue_prop_header.get_size(), 8)

    def test_pack(self):
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        queue_prop_header.pack()

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

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
