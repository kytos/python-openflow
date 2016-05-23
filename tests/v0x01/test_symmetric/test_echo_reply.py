import os
import unittest

from pyof.v0x01.symmetric import echo_reply
from pyof.v0x01.common import header as of_header


class TestEchoReply(unittest.TestCase):

    def setUp(self):
        self.message = echo_reply.EchoReply(xid=0)
        self.header = of_header.Header()

    def test_get_size(self):
        """[Symmetric/EchoReply] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Need to implement length update')
    def test_pack(self):
        """[Symmetric/EchoReply] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_reply.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_msg = b'\x01\x03\x00\x08\x00\x00\x00\x00'
        self.assertEqual(self.message.pack(), packed_msg)

    def test_unpack(self):
        """[Symmetric/Reply] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_reply.dat')
        with open(filename,'rb') as f:
            self.header.unpack(f.read(8))
            msg_size = self.header.length._value
            self.assertEqual(self.message.unpack(f.read()), None)
