import unittest

from ofp.v0x01.controller2switch import stats_request


class TestStatsRequest(unittest.TestCase):

    def setUp(self):
        self.stats_request = stats_request.StatsRequest(xid=1, req_type=3,
                                                        flags=1, body=[])

    def test_get_size(self):
        self.assertEqual(self.stats_request.get_size(), 12)

    def test_pack(self):
        self.stats_request.pack()

    def test_unpack(self):
        pass
