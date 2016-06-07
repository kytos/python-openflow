import unittest

from pyof.v0x01.controller2switch.common import DescStats
from pyof.v0x01.foundation import base


class TestDescStats(unittest.TestCase):

    def setUp(self):
        content = bytes('A' * base.DESC_STR_LEN, 'utf-8')
        self.message = DescStats()
        self.message.mfr_desc = content
        self.message.hw_desc = content
        self.message.sw_desc = content
        self.message.serial_num = content
        self.message.dp_desc = content

    def test_get_size(self):
        """[Controller2Switch/DescStats] - size 1056"""
        self.assertEqual(self.message.get_size(), 1056)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/DescStats] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/DescStats] - unpacking"""
        # TODO
        pass
