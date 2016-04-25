import unittest

from ofp.v0x01.symmetric import hello


class TestHello(unittest.TestCase):
    def setUp(self):
        self.hello = hello.OFPHello(length=8, xid=1)

    def test_get_size(self):
        self.assertEqual(self.hello.get_size(), 8)

    def test_pack(self):
        self.hello.pack()

    def test_unpack(self):
        pass
