"""MultipartReply message test."""

from pyof.v0x04.controller2switch.common import MultipartTypes
from pyof.v0x04.controller2switch.multipart_reply import (MultipartReply,
                                                          MultipartReplyFlags)

from tests.v0x04.test_struct import TestStruct


class TestTableFeatures(TestStruct):
    """Test TableFeatures."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=16,
                            multipart_type=MultipartTypes.OFPMP_METER_CONFIG,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body=b'this is a test')
        super().set_minimum_size(16)
