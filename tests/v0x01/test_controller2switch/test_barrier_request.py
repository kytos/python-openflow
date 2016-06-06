import unittest
import os

from pyof.v0x01.controller2switch import barrier_request
from pyof.v0x01.common import header as of_header

class TestBarrierRequest(unittest.TestCase):

    def setUp(self):
        self.message = barrier_request.BarrierRequest(xid=1)
        self.head = of_header.Header(xid=5)

    def test_get_size(self):
        """[Controller2Switch/BarrierRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/BarrierRequest] - packing"""
        # TODO
        pass

    def test_unpack(self):
        """[Controller2Switch/BarrierRequest] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_barrier_request.dat')
        with open(filename, 'rb') as f:
            self.head.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)
