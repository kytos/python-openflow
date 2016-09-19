"""GetAsyncRequest message tests."""
from pyof.v0x04.controller2switch.get_async_request import GetAsyncRequest
from tests.test_struct import TestStruct


class TestGetAsyncRequest(TestStruct):
    """Test the GetAsyncRequest message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_get_async_request')
        super().set_raw_dump_object(GetAsyncRequest, xid=3)
        super().set_minimum_size(8)
