import unittest

from ofp.v0x01.controller2switch import queue_get_config_reply
from ofp.v0x01.common import queue
from ofp.v0x01.common import header

class TestQueueGetConfigReply(unittest.TestCase):

    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 24, 1)
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        packet_queue = queue.PacketQueue(1, 8, [0, 0], queue_prop_header)
        queue_get_config_reply_message = \
            queue_get_config_reply.QueueGetConfigReply(header=ofp_header,
                                                       port=80,
                                                       pad=[0, 0, 0, 0, 0, 0],
                                                       queue=packet_queue)
        self.assertEqual(queue_get_config_reply_message.get_size(), 16)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 40, 1)
        queue_prop_header = queue.QueuePropHeader(1, 8, [1, 1, 1, 1])
        packet_queue = queue.PacketQueue(1, 8, [0, 0], queue_prop_header)
        queue_get_config_reply_message = \
            queue_get_config_reply.QueueGetConfigReply(header=ofp_header,
                                                       port=80,
                                                       pad=[0, 0, 0, 0, 0, 0],
                                                       queue=packet_queue)
        queue_get_config_reply_message.pack()

    def test_unpack(self):
        pass
