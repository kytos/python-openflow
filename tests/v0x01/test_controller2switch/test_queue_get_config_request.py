import unittest

from ofp.v0x01.controller2switch import queue_get_config_request
from ofp.v0x01.common import queue
from ofp.v0x01.common import header

class TestQueueGetConfigRequest(unittest.TestCase):

    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 20, 1)
        queue_get_config_request_message = \
            queue_get_config_request.QueueGetConfigRequest(header=ofp_header,
                                                           port=80, pad=[0, 0])
        self.assertEqual(queue_get_config_request_message.get_size(), 12)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 20, 1)
        queue_get_config_request_message = \
            queue_get_config_request.QueueGetConfigRequest(header=ofp_header,
                                                           port=80, pad=[0, 0])
        queue_get_config_request_message.pack()

    def test_unpack(self):
        pass
