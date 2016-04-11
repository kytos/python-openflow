import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from foundation import basic_types

class TestUBInt8(unittest.TestCase):
    def test_get_size(self):
        ubint8 = basic_types.UBInt8()
        self.assertEqual(ubint8.get_size(), 1);

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
