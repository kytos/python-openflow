"""MultipartRequest message test."""
from pyof.v0x04.controller2switch.multipart_request import MultipartRequest
from tests.test_struct import TestStruct


class TestMultipartRequest(TestStruct):
    """Test the MultipartRequest message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_multipart_request')
        super().set_raw_dump_object(MultipartRequest, xid=3, multipart_type=0,
                                    flags=1, body=0)
        super().set_minimum_size(16)
