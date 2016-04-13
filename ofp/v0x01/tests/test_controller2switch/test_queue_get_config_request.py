import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch import queue_get_config_request


class TestQueueGetConfigRequest(unittest.TestCase):

    def test_get_size(self):
        queue_get_config_request_message = queue_get_config_request.QueueGetConfigRequest()
        self.assertEqual(queue_get_config_request_message.get_size(), 12)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
