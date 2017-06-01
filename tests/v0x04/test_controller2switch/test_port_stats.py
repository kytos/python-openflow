"""Config Port Stats message tests."""
from pyof.v0x04.controller2switch.multipart_reply import PortStats
from tests.test_struct import TestStruct


class TestPortStats(TestStruct):
    """Config Port Stats message tests."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_port_stats')
        super().set_raw_dump_object(PortStats)
        super().set_minimum_size(112)
