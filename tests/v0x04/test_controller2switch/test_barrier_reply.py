"""Barrier reply message tests."""
from pyof.v0x04.controller2switch.barrier_reply import BarrierReply
from tests.test_struct import TestStruct


class TestBarrierReply(TestStruct):
    """Barrier reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_barrier_reply')
        super().set_raw_dump_object(BarrierReply, xid=5)
        super().set_minimum_size(8)
