"""Config Reply message tests."""
from pyof.v0x04.controller2switch.get_config_reply import GetConfigReply
from tests.test_struct import TestStruct


class TestGetConfigReply(TestStruct):
    """Config Reply message tests."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_get_config_reply')
        super().set_raw_dump_object(GetConfigReply, xid=1)
        super().set_minimum_size(12)
