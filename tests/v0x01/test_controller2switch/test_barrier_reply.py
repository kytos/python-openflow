"""Barrier reply message tests."""
from pyof.v0x01.controller2switch.barrier_reply import BarrierReply
from tests.test_struct import TestMsgDumpFile


class TestBarrierReply(TestMsgDumpFile):
    """Barrier reply message tests."""

    dumpfile = 'v0x01/ofpt_barrier_reply.dat'
    obj = BarrierReply(xid=5)
    min_size = 8
