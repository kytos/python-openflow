"""Test DescStats message."""
from pyof.foundation.constants import DESC_STR_LEN
from pyof.v0x01.controller2switch.common import DescStats, StatsTypes
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestDescStats(TestMsgDumpFile):
    """Test class for TestDescStats."""

    dumpfile = 'v0x01/ofpt_desc_stats_reply.dat'

    content = 'A' * DESC_STR_LEN
    desc = DescStats(mfr_desc=content, hw_desc=content,
                     sw_desc=content, serial_num=content,
                     dp_desc=content)
    obj = StatsReply(xid=14,
                     body_type=StatsTypes.OFPST_DESC,
                     flags=0, body=desc)
    min_size = 12
