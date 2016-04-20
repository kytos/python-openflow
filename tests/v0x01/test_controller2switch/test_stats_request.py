import unittest

from ofp.v0x01.common import header
from ofp.v0x01.controller2switch import stats_request

class TestStatsRequest(unittest.TestCase):
    def test_get_size(self):
        ofp_header1 = header.OFPHeader(1, 16, 1)
        stats_request_message1 = \
            stats_request.StatsRequest(header=ofp_header1, req_type=3, flags=1,
                                        body=[1, 1, 1, 1])
        self.assertEqual(stats_request_message1.get_size(), 16)
        ofp_header2 = header.OFPHeader(1, 18, 1)
        stats_request_message2 = \
            stats_request.StatsRequest(header=ofp_header2, req_type=3, flags=1,
                                        body=[1, 1, 1, 1, 1, 1])
        self.assertEqual(stats_request_message2.get_size(), 18)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 16, 1)
        stats_request_message = \
            stats_request.StatsRequest(header=ofp_header, req_type=3, flags=1,
                                        body=[1, 1, 1, 1])
        stats_request_message.pack()

    def test_unpack(self):
        pass
