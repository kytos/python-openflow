import unittest

from pyof.v0x01.controller2switch.common import QueueStatsRequest


class TestQueueStatsRequest(unittest.TestCase):

    def setUp(self):
        self.message = QueueStatsRequest()
        self.message.port_no = 80
        self.message.queue_id = 5

    def test_get_size(self):
        """[Controller2Switch/QueueStatsRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/QueueStatsRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/QueueStatsRequest] - unpacking"""
        # TODO
        pass
