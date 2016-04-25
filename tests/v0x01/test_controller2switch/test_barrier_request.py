import unittest

from ofp.v0x01.controller2switch import barrier_request


class TestBarrierRequest(unittest.TestCase):
    def setUp(self):
        self.barrier_request = barrier_request.BarrierRequest(xid=1)

    def test_get_size(self):
        self.assertEqual(self.barrier_request.get_size(), 8)

    def test_pack(self):
        self.barrier_request.pack()

    def test_unpack(self):
        pass
