import unittest
import sys
import os

# OFP Modules to be tested
from ofp.v0x01.controller2switch import barrier_request

class TestBarrierRequest(unittest.TestCase):
    def test_get_size(self):
        barrier_request_message = barrier_request.BarrierRequest(xid=1)
        self.assertEqual(barrier_request_message.get_size(), 8)

    def test_pack(self):
        barrier_request_message = barrier_request.BarrierRequest(xid=1)
        barrier_request_message.pack()

    def test_unpack(self):
        pass
