import unittest

from pyof.v0x01.controller2switch.common import AggregateStatsReply


class TestAggregateStatsReply(unittest.TestCase):

    def setUp(self):
        self.message = AggregateStatsReply()
        self.message.packet_count = 5
        self.message.byte_count = 1
        self.message.flow_count = 8

    def test_get_size(self):
        """[Controller2Switch/AggregateStatsReply] - size 24"""
        self.assertEqual(self.message.get_size(), 24)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/AggregateStatsReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/AggregateStatsReply] - unpacking"""
        # TODO
        pass
