import os
import unittest

from ofp.v0x01.symmetric import echo_reply


class TestReply(unittest.TestCase):

    def setUp(self):
        self.message = echo_reply.Reply(xid=0)

    def test_get_size(self):
        """[Symmetric/Reply] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        """[Symmetric/Reply] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_reply.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_msg = b'\x01\x03\x00\x08\x00\x00\x00\x00'
        self.assertEqual(self.message.pack(), packed_msg)

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Symmetric/Reply] - unpacking"""
        # TODO
        pass
