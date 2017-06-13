"""Testing Error Message."""
from pyof.v0x01.asynchronous.error_msg import (
    BadRequestCode, ErrorMsg, ErrorType, FlowModFailedCode)
from tests.test_struct import TestStruct


class TestErrorMessage(TestStruct):
    """Test the Error Message."""

    @classmethod
    def setUpClass(cls):
        """Setup TestStruct."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_error_msg')
        super().set_raw_dump_object(ErrorMsg, xid=12,
                                    error_type=ErrorType.OFPET_BAD_REQUEST,
                                    code=BadRequestCode.OFPBRC_BAD_STAT,
                                    data=b'')
        super().set_minimum_size(12)

    def test_unpack_error_msg(self):
        """Test Unpack a sample ErrorMsg."""
        expected = b'\x01\x01\x00\x1b\x00\x00\x00\x18\x00\x03\x00\x02FLOW'

        error_msg = ErrorMsg(xid=24,
                             error_type=ErrorType.OFPET_FLOW_MOD_FAILED,
                             code=FlowModFailedCode.OFPFMFC_EPERM,
                             data=b'FLOW')

        actual = ErrorMsg(xid=24)
        actual.unpack(expected[8:])

        self.assertEqual(actual, error_msg)
