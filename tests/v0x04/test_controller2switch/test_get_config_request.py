"""Config Request message tests."""
from pyof.v0x04.controller2switch.get_config_request import GetConfigRequest
from tests.test_struct import TestStruct


class TestGetConfigRequest(TestStruct):
    """Config Request message tests."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_get_config_request')
        super().set_raw_dump_object(GetConfigRequest)
        super().set_minimum_size(8)
