import unittest

from ofp.v0x01.controller2switch import barrier_reply


class TestBarrierReply(unittest.TestCase):
    def setUp(self):
        self.barrier_reply = barrier_reply.BarrierReply(xid=1)

    def test_get_size(self):
        self.assertEqual(self.barrier_reply.get_size(), 8)

    def test_pack(self):
        self.barrier_reply.pack()

    def test_unpack(self):
        pass
