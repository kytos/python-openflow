import unittest

from ofp.v0x01.controller2switch import table_stats

class TestTableStats(unittest.TestCase):
    def test_get_size(self):
        table_stats_message = \
            table_stats.TableStats(table_id=1, pad=[0, 0, 0],
                                   name=[bytes('X','utf-8') for _ in range(32)],
                                   wildcards=1, max_entries=1, active_count=10,
                                   count_lookup=10, count_matched=0)
        self.assertEqual(table_stats_message.get_size(), 64)

    def test_pack(self):
        table_stats_message = \
            table_stats.TableStats(table_id=1, pad=[0, 0, 0],
                                   name=[bytes('X','utf-8') for _ in range(32)],
                                   wildcards=1, max_entries=1, active_count=10,
                                   count_lookup=10, count_matched=0)
        table_stats_message.pack()

    def test_unpack(self):
        pass
