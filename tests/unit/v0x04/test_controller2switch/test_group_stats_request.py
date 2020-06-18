"""Group stats request message."""
from pyof.v0x04.controller2switch.common import MultipartType
from pyof.v0x04.controller2switch.multipart_request import (
    GroupStatsRequest, MultipartRequest)
from tests.unit.test_struct import TestStruct


class TestGroupStatsRequest(TestStruct):
    """Group stats request message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_group_stats_request')
        super().set_raw_dump_object(MultipartRequest, xid=1,
                                    multipart_type=MultipartType.OFPMP_GROUP,
                                    flags=0, body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartRequest message."""
    return GroupStatsRequest()
