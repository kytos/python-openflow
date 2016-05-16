import unittest

from pyof.v0x01.common import flow_match
from pyof.v0x01.controller2switch import table_stats
from pyof.v0x01.foundation import base


class TestTableStats(unittest.TestCase):

    def setUp(self):
        self.message = table_stats.TableStats()
        self.message.table_id = 1
        self.message.name = bytes('X' * base.OFP_MAX_TABLE_NAME_LEN, 'utf-8')
        self.message.wildcards = flow_match.FlowWildCards.OFPFW_TP_DST
        self.message.max_entries = 1
        self.message.active_count = 10
        self.message.count_lookup = 10
        self.message.count_matched = 0

    def test_get_size(self):
        """[Controller2Switch/TableStats] - size 64"""
        self.assertEqual(self.message.get_size(), 64)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/TableStats] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/TableStats] - unpacking"""
        # TODO
        pass
