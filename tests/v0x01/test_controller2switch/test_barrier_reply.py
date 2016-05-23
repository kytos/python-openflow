import unittest
import os

from pyof.v0x01.controller2switch import barrier_reply
from pyof.v0x01.common import header as of_header


class TestBarrierReply(unittest.TestCase):

    def setUp(self):
        self.message = barrier_reply.BarrierReply(xid=5)
        self.head = of_header.Header()

    def test_get_size(self):
        """[Controller2Switch/BarrierReply] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Need to implement length update')
    def test_pack(self):
        """[Controller2Switch/BarrierReply] - packing"""
        packed_msg = b'\x01\x13\x00\x08\x00\x00\x00\x05'
        self.assertEqual(self.message.pack(), packed_msg)

    def test_unpack(self):
        """[Controller2Switch/BarrierReply] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_barrier_reply.dat')
        with open(filename,'rb') as f:
            self.head.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)
