import unittest

from ofp.v0x01.symmetric import echo_reply

class TestOFPReply(unittest.TestCase):
    def test_get_size(self):
        reply_message = echo_reply.OFPReply(xid=3)
        self.assertEqual(reply_message.get_size(), 8)

    def test_pack(self):
        reply_message = echo_reply.OFPReply(xid=3)
        reply_message.pack()

    def test_unpack(self):
        pass
