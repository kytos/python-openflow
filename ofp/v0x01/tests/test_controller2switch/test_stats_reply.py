import unittest

from ofp.v0x01.common import header
from ofp.v0x01.controller2switch import stats_reply

class TestStatsReply(unittest.TestCase):
    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 20, 1)
        stats_reply_message = stats_reply.StatsReply(header=ofp_header,
                                                     ofpsf_req_type=3,
                                                     flags=1, body=[])
        self.assertEqual(stats_reply_message.get_size(), 12)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 20, 1)
        stats_reply_message = stats_reply.StatsReply(header=ofp_header,
                                                     ofpsf_req_type=3,
                                                     flags=1, body=[])
        stats_reply_message.pack()

    def test_unpack(self):
        pass
