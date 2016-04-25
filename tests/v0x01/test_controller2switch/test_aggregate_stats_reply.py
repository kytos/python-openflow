import unittest

from ofp.v0x01.controller2switch import aggregate_stats_reply as asr


class TestAggregateStatsReply(unittest.TestCase):
    def setUp(self):
        self.agg_stats_reply = asr.AggregateStatsReply(packet_count=5,
                                                       byte_count=1,
                                                       flow_count=8,
                                                       pad=[1, 2, 3, 4])

    def test_get_size(self):
        self.assertEqual(self.agg_stats_reply.get_size(), 24)

    def test_pack(self):
        self.agg_stats_reply.pack()

    def test_unpack(self):
        pass
