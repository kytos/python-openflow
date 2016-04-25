import unittest

from ofp.v0x01.controller2switch import table_stats
from ofp.v0x01.foundation import base


class TestTableStats(unittest.TestCase):
    def setUp(self):
        name = bytes("".join(['X' for _ in range(base.OFP_MAX_TABLE_NAME_LEN)]),
                     'utf-8')
        self.table_stats = table_stats.TableStats(table_id=1, pad=[0, 0, 0],
                                                  name=name, wildcards=1,
                                                  max_entries=1,
                                                  active_count=10,
                                                  count_lookup=10,
                                                  count_matched=0)

    def test_get_size(self):
        self.assertEqual(self.table_stats.get_size(), 64)

    def test_pack(self):
        self.table_stats.pack()

    def test_unpack(self):
        pass
