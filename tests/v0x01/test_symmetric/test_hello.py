import os
import unittest

from pyof.v0x01.symmetric import hello
from pyof.v0x01.common import header as of_header

class TestHello(unittest.TestCase):

    def setUp(self):
        self.message = hello.Hello(xid=1)
        self.header = of_header.Header()

    def test_get_size(self):
        """[Symmetric/Hello] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Need to implement length update')
    def test_pack(self):
        """[Symmetric/Hello] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_hello.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_hello = b'\x01\x00\x00\x08\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_hello)

    def test_unpack(self):
        """[Symmetric/Hello] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_hello.dat')
        with open(filename, 'rb') as f:
            self.header.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)
