"""Test GetConfigRequest message."""
from pyof.v0x01.controller2switch.get_config_request import GetConfigRequest
from tests.test_struct import TestMsgDumpFile


class TestGetConfigRequest(TestMsgDumpFile):
    """Test class for TestGetConfigReply."""

    dumpfile = 'v0x01/ofpt_get_config_request.dat'
    obj = GetConfigRequest(xid=1)
    min_size = 9
