import unittest

from pyof.v0x01.controller2switch import common
from pyof.v0x01.controller2switch import stats_request


class TestStatsRequest(unittest.TestCase):

    def setUp(self):
        self.message = stats_request.StatsRequest()
        self.message.header.xid = 1
        self.message.type = common.StatsTypes.OFPST_FLOW
        self.message.flags = 1
        self.message.body = []

    def test_get_size(self):
        """[Controller2Switch/StatsRequest] - size 12"""
        self.assertEqual(self.message.get_size(), 12)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/StatsRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/StatsRequest] - unpacking"""
        # TODO
        pass
