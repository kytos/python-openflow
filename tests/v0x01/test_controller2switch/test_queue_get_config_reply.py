import unittest

from pyof.v0x01.controller2switch import queue_get_config_reply
from pyof.v0x01.common import queue


class TestQueueGetConfigReply(unittest.TestCase):

    def setUp(self):
        propertie01 = queue.QueuePropHeader()
        propertie01.property = queue.QueueProperties.OFPQT_MIN_RATE
        propertie01.len = 12
        packet_queue = queue.PacketQueue()
        packet_queue.queue_id = 1
        packet_queue.length = 8
        packet_queue.properties = [propertie01]
        self.message = queue_get_config_reply.QueueGetConfigReply()
        self.message.header.xid = 1
        self.message.port = 80
        self.message.queue = packet_queue

    def test_get_size(self):
        """[Controller2Switch/QueueGetConfigReply] - size 16"""
        self.assertEqual(self.message.get_size(), 16)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/QueueGetConfigReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/QueueGetConfigReply] - unpacking"""
        # TODO
        pass
