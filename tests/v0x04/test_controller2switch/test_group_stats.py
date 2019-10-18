"""Group stats message."""
from pyof.v0x04.common.action import ActionOutput, ListOfActions
from pyof.v0x04.common.flow_instructions import (
    InstructionApplyAction, ListOfInstruction)
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.common import (
    BucketCounter, ListOfBucketCounter, MultipartType)
from pyof.v0x04.controller2switch.multipart_reply import (
    GroupStats, MultipartReply)
from tests.test_struct import TestStruct


class TestGroupStats(TestStruct):
    """Group stats message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_group_stats')
        super().set_raw_dump_object(MultipartReply, xid=1,
                                    multipart_type=MultipartType.OFPMP_GROUP,
                                    flags=0,
                                    body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartReply message."""
    bs = ListOfBucketCounter([BucketCounter(packet_count=0, byte_count=0),
                              BucketCounter(packet_count=0, byte_count=0)])
    return GroupStats(length=72, group_id=1, ref_count=0,
                      packet_count=0, byte_count=0, duration_sec=14,
                      duration_nsec=837000000, bucket_stats=bs)
