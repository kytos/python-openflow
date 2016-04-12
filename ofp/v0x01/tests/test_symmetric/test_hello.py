import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from symmetric.hello import OFPHello

class TestHello(unittest.TestCase):
    def test_get_size(self):
        hello = OFPHello(1)
        self.assertEqual(hello.get_size(), 8)

    def test_pack(self):
        hello = OFPHello(1)
        hello.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
