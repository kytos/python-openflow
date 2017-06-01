"""Experimenter message tests."""
from pyof.v0x04.symmetric.experimenter import ExperimenterHeader
from tests.test_struct import TestStruct


class TestExperimenter(TestStruct):
    """Experimenter message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_experimenter')
        super().set_raw_dump_object(ExperimenterHeader, xid=1, experimenter=1,
                                    exp_type=0)
        super().set_minimum_size(16)
