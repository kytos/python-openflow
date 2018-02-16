"""Test for StatsRequest message."""
from pyof.v0x01.controller2switch.common import StatsType
from pyof.v0x01.controller2switch.stats_request import StatsRequest
from tests.test_struct import TestStruct


class TestStatsRequest(TestStruct):
    """Test for StatsRequest message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/StatsRequest] - size 12."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_stats_request')
        super().set_raw_dump_object(StatsRequest, xid=1,
                                    body_type=StatsType.OFPST_FLOW,
                                    flags=1, body=b'')
        super().set_minimum_size(12)
