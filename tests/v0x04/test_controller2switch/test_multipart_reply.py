"""MultipartReply message test."""

from pyof.v0x04.controller2switch.common import MultipartTypes
from pyof.v0x04.controller2switch.multipart_reply import (
    Desc, MultipartReply, MultipartReplyFlags)
from tests.v0x04.test_struct import TestStruct


class TestMultipartReply(TestStruct):
    """Test MultipartReply."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=16,
                            multipart_type=MultipartTypes.OFPMP_METER_CONFIG,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body='')
        super().set_minimum_size(16)

    @staticmethod
    def get_attributes(multipart_type=MultipartTypes.OFPMP_DESC,
                       flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                       body=''):
        """Method used to return a dict with instance paramenters."""
        return {'xid': 32, 'multipart_type': multipart_type, 'flags': flags,
                'body': body}

    def test_pack_unpack_desc(self):
        """Testing multipart_type with OFPMP_DESC."""
        instances = Desc(mfr_desc="MANUFACTURER DESCRIPTION",
                         hw_desc="HARDWARE DESCRIPTION",
                         sw_desc="SOFTWARE DESCRIPTION",
                         serial_num="SERIAL NUMBER",
                         dp_desc="DATAPATH DESCRIPTION")
        options = TestMultipartReply.get_attributes(
            multipart_type=MultipartTypes.OFPMP_DESC, body=instances)
        self._test_pack_unpack(**options)
