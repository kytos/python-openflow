import unittest

from ofp.v0x01.symmetric import hello


class TestHello(unittest.TestCase):

    def setUp(self):
        self.message = hello.OFPHello(xid=1)

    def test_get_size(self):
        """[Symmetric/Hello] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        """[Symmetric/Hello] - packing"""
        packed_hello = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_hello)

    def test_unpack(self):
        """[Symmetric/Hello] - unpacking"""
        # TODO
        pass
