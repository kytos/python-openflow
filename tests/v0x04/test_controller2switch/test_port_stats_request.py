"""Config Port Stats Request message tests."""
from pyof.v0x04.controller2switch.multipart_request import PortStatsRequest
from tests.test_struct import TestStruct


class TestPortStatsRequest(TestStruct):
    """Config Port Stats Request message tests."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_port_stats_request')
        super().set_raw_dump_object(PortStatsRequest)
        super().set_minimum_size(8)
