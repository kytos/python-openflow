import unittest

from ofp.v0x01.symmetric import echo_reply


class TestOFPReply(unittest.TestCase):
    def setUp(self):
        self.message = echo_reply.OFPReply(xid=3)

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
