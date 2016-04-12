import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import queue
from foundation.basic_types import UBInt8Array

class TestPacketQueue(unittest.TestCase):
    def test_get_size(self):
        pq = queue.PacketQueue(1, 8, UBInt8Array(value=0, length=2))
        self.assertEqual(pq.get_size(), 8)

    def test_pack(self):
        pq = queue.PacketQueue(1, 8, UBInt8Array(value=0, length=2))
        pq.pack()

    def test_unpack(self):
        pass

class TestQueuePropHeader(unittest.TestCase):
    def test_get_size(self):
        qph = queue.QueuePropHeader(1, 8, UBInt8Array(value=0, length=4))
        self.assertEqual(qph.get_size(), 8)

    def test_pack(self):
        qph = queue.QueuePropHeader(1, 8, UBInt8Array(value=0, length=4))
        qph.pack()

    def test_unpack(self):
        pass

class TestQueuePropMinRate(unittest.TestCase):
    def test_get_size(self):
        qpmr = queue.QueuePropMinRate(1000, 100000, UBInt8Array(value=0, length=6))
        self.assertEqual(qpmr.get_size(), 16)

    def test_pack(self):
        qpmr = queue.QueuePropMinRate(1000, 100000, UBInt8Array(value=0, length=6))
        qpmr.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
