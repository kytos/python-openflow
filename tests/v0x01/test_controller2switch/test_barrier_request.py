"""Barrier request message tests."""
from pyof.v0x01.controller2switch.barrier_request import BarrierRequest
from tests.test_struct import TestMsgDumpFile


class TestBarrierRequest(TestMsgDumpFile):
    """Barrier request message tests."""

    dumpfile = 'v0x01/ofpt_barrier_request.dat'
    obj = BarrierRequest(xid=5)
    min_size = 8
