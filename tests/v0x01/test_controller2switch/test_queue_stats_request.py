import unittest

from ofp.v0x01.controller2switch import queue_stats_request


class TestQueueStatsRequest(unittest.TestCase):
    def setUp(self):
        self.message = queue_stats_request.QueueStatsRequest(port_no=80,
                                                             pad=[0, 0],
                                                             queue_id=5)

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
