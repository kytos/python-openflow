"""Testing Error Message."""
from pyof.v0x01.asynchronous.error_msg import (
    BadRequestCode, ErrorMsg, ErrorType, FlowModFailedCode)
from tests.test_struct import TestMsgDump, TestMsgDumpFile


class TestErrorMessage_fromfile(TestMsgDumpFile):
    """Test the ErrorMsg class."""

    dumpfile = 'v0x01/ofpt_error_msg.dat'
    obj = ErrorMsg(xid=12,
                   error_type=ErrorType.OFPET_BAD_REQUEST,
                   code=BadRequestCode.OFPBRC_BAD_STAT,
                   data=b'')
    min_size = 12


class TestErrorMessage_dump(TestMsgDump):
    """Test the ErrorMsg class."""

    # dump needs to be checked
    dump = b'\x01\x01\x00\x10\x00\x00\x00\x18\x00\x03\x00\x02FLOW'
    obj = ErrorMsg(xid=24,
                   error_type=ErrorType.OFPET_FLOW_MOD_FAILED,
                   code=FlowModFailedCode.OFPFMFC_EPERM,
                   data=b'FLOW')
    min_size = 12
