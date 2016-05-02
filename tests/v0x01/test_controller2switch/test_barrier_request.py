import unittest

from ofp.v0x01.controller2switch import barrier_request


class TestBarrierRequest(unittest.TestCase):

    def setUp(self):
        self.message = barrier_request.BarrierRequest(xid=1)

    def test_get_size(self):
        """[Controller2Switch/BarrierRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/BarrierRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/BarrierRequest] - unpacking"""
        # TODO
        pass
