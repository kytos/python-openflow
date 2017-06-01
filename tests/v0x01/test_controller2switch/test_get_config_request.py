"""Test GetConfigRequest message."""
from pyof.v0x01.controller2switch.get_config_request import GetConfigRequest
from tests.test_struct import TestStruct


class TestGetConfigRequest(TestStruct):
    """Test class for TestGetConfigRequest."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/GetConfigRequest] - size 8."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_get_config_request')
        super().set_raw_dump_object(GetConfigRequest, xid=1)
        super().set_minimum_size(8)
