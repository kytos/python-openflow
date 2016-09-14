"""Testing ErrorMessage."""
from pyof.v0x01.asynchronous.error_msg import (BadRequestCode, ErrorMsg,
                                               ErrorType)
from pyof.v0x01.symmetric.hello import Hello

from ...test_struct import TestStruct


class TestErrorMsg(TestStruct):
    """Test the ErrorMsg message."""

    @classmethod
    def setUpClass(cls):
        """Setup TestStruct."""
        super().setUpClass()
        super().set_minimum_size(12, ErrorMsg)

    def setUp(self):
        """Error message to be used in multiple tests."""
        self.error_msg = ErrorMsg(error_type=ErrorType.OFPET_BAD_REQUEST,
                                  code=BadRequestCode.OFPBRC_BAD_STAT,
                                  data=b'')

    def test_pack_unpack_with_empty_data(self):
        """Should accept and empty byte as data."""
        # unpacked data
        u_error = ErrorMsg()
        u_error.unpack(self.error_msg.pack())

        self.assertEqual(self.error_msg.error_type, u_error.error_type)
        self.assertEqual(self.error_msg.code, u_error.code)
        self.assertEqual(b'', u_error.data)

    def test_pack_unpack_with_hello(self):
        """`Hello` message in `data` field after packing and unpacking."""
        # packed data
        p_hello = Hello()
        self.error_msg.data = p_hello
        packed = self.error_msg.pack()

        # unpacked data
        u_error = ErrorMsg()
        u_error.unpack(packed)
        u_hello = u_error.data

        self.assertEqual(p_hello, u_hello)
