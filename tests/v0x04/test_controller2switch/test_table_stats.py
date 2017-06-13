"""Table stats message."""
from pyof.v0x04.controller2switch.multipart_reply import TableStats
from tests.test_struct import TestStruct


class TestTableStats(TestStruct):
    """Table stats message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_table_stats')
        super().set_raw_dump_object(TableStats)
        super().set_minimum_size(24)
