import os
import unittest

from ofp.v0x01.symmetric import echo_request


class TestEchoRequest(unittest.TestCase):

    def setUp(self):
        self.message = echo_request.EchoRequest(xid=0)

    def test_get_size(self):
        """[Symmetric/Request] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        """[Symmetric/Request] - packing"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_echo_request.dat')
        with open(filename, 'rb') as f:
            self.assertEqual(self.message.pack(), f.read())
        packed_msg = b'\x01\x02\x00\x08\x00\x00\x00\x00'
        self.assertEqual(self.message.pack(), packed_msg)

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Symmetric/Request] - unpacking"""
        # TODO
        pass
