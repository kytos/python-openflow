"""Test TableStats message."""
from pyof.foundation.constants import OFP_MAX_TABLE_NAME_LEN
from pyof.v0x01.common.flow_match import FlowWildCards
from pyof.v0x01.controller2switch.common import StatsTypes, TableStats
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from tests.test_struct import TestMsgDumpFile


class TestTableStats(TestMsgDumpFile):
    """Test class for TableStats."""

    dumpfile = 'v0x01/ofpt_table_stats.dat'

    table_stats = TableStats(
        table_id=1,
        name='X' * OFP_MAX_TABLE_NAME_LEN,
        wildcards=FlowWildCards.OFPFW_TP_DST, max_entries=1,
        active_count=10, count_lookup=10, count_matched=0)
    obj = StatsReply(xid=14, body_type=StatsTypes.OFPST_TABLE,
                     flags=0, body=table_stats)
    min_size = 12
