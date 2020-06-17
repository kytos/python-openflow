"""Testing v0x04 error message class."""
from pyof.foundation.exceptions import MethodNotImplemented
from pyof.v0x04.asynchronous.error_msg import (
    ErrorExperimenterMsg, ErrorMsg, ErrorType, MeterModFailedCode)
from tests.unit.test_struct import TestStruct


class TestErrorMsg(TestStruct):
    """ErroMsg message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        error_type = ErrorType.OFPET_METER_MOD_FAILED
        code = MeterModFailedCode.OFPMMFC_UNKNOWN_METER
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_error')
        super().set_raw_dump_object(ErrorMsg, xid=1, error_type=error_type,
                                    code=code, data=_get_data())
        super().set_minimum_size(12)

    @staticmethod
    def test_unpack():
        """[Asynchronous/error_msg] - unpack ErrorExperimenterMsg."""
        unpacked = ErrorExperimenterMsg()
        try:
            unpacked.unpack("pack")
        except MethodNotImplemented:
            pass


def _get_data():
    """Return data for ErrorMsg object."""
    data = b'\x04\x12\x00\x18\x00\x00\x00\x01\x00\x0a\x00\x00\x00\x00\x00'
    data += b'\x00\x00\x00\x00\x01\x00\x00\x00\x00'
    return data
