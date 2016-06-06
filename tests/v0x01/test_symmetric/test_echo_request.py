import os
import unittest

from pyof.v0x01.symmetric import echo_request
from pyof.v0x01.common import header as of_header


class TestEchoRequest(unittest.TestCase):

    def setUp(self):
        self.message = echo_request.EchoRequest(xid=0)
        self.header = of_header.Header()

    def test_get_size(self):
        """[Symmetric/EchoRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Need to implement length update')
    def test_pack(self):
        """[Symmetric/EchoRequest] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_request.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_msg = b'\x01\x02\x00\x08\x00\x00\x00\x00'
        self.assertEqual(self.message.pack(), packed_msg)

    def test_unpack(self):
        """[Symmetric/EchoRequest] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_request.dat')
        with open(filename,'rb') as f:
            self.header.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)
