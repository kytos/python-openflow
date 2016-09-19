"""Barrier request message tests."""
from pyof.v0x04.controller2switch.barrier_request import BarrierRequest
from tests.test_struct import TestStruct


class TestBarrierRequest(TestStruct):
    """Barrier reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_barrier_request')
        super().set_raw_dump_object(BarrierRequest, xid=5)
        super().set_minimum_size(8)
