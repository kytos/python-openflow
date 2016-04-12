import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.queue_get_config_request import QueueGetConfigRequest

class TestQueueGetConfigRequest(unittest.TestCase):
    def test_get_size(self):
        qgcr = QueueGetConfigRequest()
        self.assertEqual(qgcr.get_size(), 12)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
