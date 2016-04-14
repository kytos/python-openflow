import unittest

from ofp.v0x01.controller2switch import desc_stats
from ofp.v0x01.foundation import base

class TestDescStats(unittest.TestCase):
    def test_get_size(self):
        mfr_desc = bytes("".join(['A' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        hw_desc = bytes("".join(['B' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        sw_desc = bytes("".join(['C' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        serial_num = bytes("".join(['9' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        dp_desc = bytes("".join(['X' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        desc_stats_message = desc_stats.DescStats(mfr_desc, hw_desc, sw_desc,
                                                  serial_num, dp_desc)
        self.assertEqual(desc_stats_message.get_size(), 1056)

    def test_pack(self):
        mfr_desc = bytes("".join(['A' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        hw_desc = bytes("".join(['B' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        sw_desc = bytes("".join(['C' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        serial_num = bytes("".join(['9' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        dp_desc = bytes("".join(['X' for _ in range(base.DESC_STR_LEN)]), 'utf-8')
        desc_stats_message = desc_stats.DescStats(mfr_desc, hw_desc, sw_desc,
                                                  serial_num, dp_desc)
        desc_stats_message.pack()

    def test_unpack(self):
        pass
