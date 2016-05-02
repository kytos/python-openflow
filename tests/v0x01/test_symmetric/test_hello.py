import os
import unittest

from ofp.v0x01.symmetric import hello


class TestHello(unittest.TestCase):

    def setUp(self):
        self.message = hello.Hello(xid=1)

    def test_get_size(self):
        """[Symmetric/Hello] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        """[Symmetric/Hello] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_hello.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_hello = b'\x01\x00\x00\x08\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_hello)

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Symmetric/Hello] - unpacking"""
        # TODO
        pass
