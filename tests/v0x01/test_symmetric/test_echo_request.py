import unittest

from ofp.v0x01.symmetric import echo_request


class TestOFPRequest(unittest.TestCase):
    def setUp(self):
        self.message = echo_request.OFPRequest(xid=2)

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
