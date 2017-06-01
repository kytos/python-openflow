"""Test for PortStatsRequest."""
from pyof.v0x01.controller2switch.common import PortStatsRequest, StatsTypes
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestStruct


class TestPortStatsRequest(TestStruct):
    """Test for PortStatsRequest."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/PortStatsRequest] - size 8."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_port_stats_request')
        super().set_raw_dump_object(StatsRequest, xid=17,
                                    body_type=StatsTypes.OFPST_PORT,
                                    flags=0, body=PortStatsRequest(port_no=80))
        super().set_minimum_size(12)
