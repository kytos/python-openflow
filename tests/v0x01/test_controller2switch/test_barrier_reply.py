import unittest

from pyof.v0x01.controller2switch import barrier_reply


class TestBarrierReply(unittest.TestCase):

    def setUp(self):
        self.message = barrier_reply.BarrierReply(xid=1)

    def test_get_size(self):
        """[Controller2Switch/BarrierReply] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/BarrierReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/BarrierReply] - unpacking"""
        # TODO
        pass
