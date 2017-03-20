"""Testing Error Message."""
from pyof.foundation.basic_types import BinaryData
from pyof.v0x01.asynchronous.error_msg import (BadRequestCode, ErrorMsg,
                                               ErrorType)

from tests.test_struct import TestStruct


class TestErrorMessage(TestStruct):
    """Test the Error Message."""

    @classmethod
    def setUpClass(cls):
        """Setup TestStruct."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_error_message')
        super().set_raw_dump_object(ErrorMsg, xid=12,
                                    error_type=ErrorType.OFPET_BAD_REQUEST,
                                    code=BadRequestCode.OFPBRC_BAD_STAT,
                                    data=BinaryData('object_test'))
        super().set_minimum_size(12)
