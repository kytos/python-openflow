import unittest

from ofp.v0x01.controller2switch import queue_stats


class TestQueueStats(unittest.TestCase):
    def setUp(self):
        self.message = queue_stats.QueueStats(port_no=80, pad=[0, 0],
                                              queue_id=5, tx_bytes=1,
                                              tx_packets=3, tx_errors=2)

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 32)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
