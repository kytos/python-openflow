"""Aggregate stats request message."""
from pyof.v0x04.controller2switch.common import MultipartType
from pyof.v0x04.controller2switch.multipart_reply import (
    AggregateStatsReply, MultipartReply)
from tests.unit.test_struct import TestStruct


class TestAggregateStats(TestStruct):
    """Aggregate stats message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        mp_type = MultipartType.OFPMP_AGGREGATE
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_aggregate_stats')
        super().set_raw_dump_object(MultipartReply, xid=1,
                                    multipart_type=mp_type,
                                    flags=0,
                                    body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartReply message."""
    return AggregateStatsReply(packet_count=2, byte_count=220, flow_count=2)
