"""Aggregate stats request message."""
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.controller2switch.common import MultipartType
from pyof.v0x04.controller2switch.multipart_request import (
    AggregateStatsRequest, MultipartRequest)
from tests.test_struct import TestStruct


class TestAggregateStatsRequest(TestStruct):
    """Aggregate stats request message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        mp_type = MultipartType.OFPMP_AGGREGATE
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_aggregate_stats_request')
        super().set_raw_dump_object(MultipartRequest, xid=1,
                                    multipart_type=mp_type,
                                    flags=0, body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartRequest message."""
    return AggregateStatsRequest(match=Match())
