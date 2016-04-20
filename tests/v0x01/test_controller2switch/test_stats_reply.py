import unittest

from ofp.v0x01.controller2switch import stats_reply


class TestStatsReply(unittest.TestCase):
    def setUp(self):
        self.stats_reply = stats_reply.StatsReply(xid=1, type=3,
                                                  flags=1, body=[])

    def test_get_size(self):
        self.assertEqual(self.stats_reply.get_size(), 12)

    def test_pack(self):
        self.stats_reply.pack()

    def test_unpack(self):
        pass
