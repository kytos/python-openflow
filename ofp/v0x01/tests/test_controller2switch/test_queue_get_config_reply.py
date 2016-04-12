import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.queue_get_config_reply import QueueGetConfigReply

class TestQueueGetConfigReply(unittest.TestCase):
    def test_get_size(self):
        qgcr = QueueGetConfigReply()
        self.assertEqual(qgcr.get_size(), 16)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
