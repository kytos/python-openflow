import unittest
import sys
import os

# OFP Modules to be tested
sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch import barrier_reply

class TestBarrierReply(unittest.TestCase):
    def test_get_size(self):
        barrier_reply_message = barrier_reply.BarrierReply(xid=1)
        self.assertEqual(barrier_reply_message.get_size(), 8)

    def test_pack(self):
        barrier_reply_message = barrier_reply.BarrierReply(xid=1)
        barrier_reply_message.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
