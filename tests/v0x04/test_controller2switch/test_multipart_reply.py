"""MultipartReply message test."""
from pyof.v0x04.controller2switch.multipart_reply import MultipartReply
from tests.test_struct import TestStruct


class TestMultipartReply(TestStruct):
    """Test the MultipartReply message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_multipart_reply')
        super().set_raw_dump_object(MultipartReply, xid=3, multipart_type=0,
                                    flags=1, body=0)
        super().set_minimum_size(16)
