import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from symmetric import hello


class TestHello(unittest.TestCase):

    def test_get_size(self):
        hello_message = hello.OFPHello(1)
        self.assertEqual(hello_message.get_size(), 8)

    def test_pack(self):
        hello_message = hello.OFPHello(1)
        hello_message.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
