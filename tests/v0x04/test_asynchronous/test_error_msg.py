"""Testing v0x04 error message class."""
from pyof.v0x04.asynchronous.error_msg import ErrorMsg
from tests.test_struct import TestStruct


class TestErrorMsg(TestStruct):
    """ErroMsg message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_error_msg')
        super().set_raw_dump_object(ErrorMsg, xid=1, error_type=1, code=1)
        super().set_minimum_size(12)
