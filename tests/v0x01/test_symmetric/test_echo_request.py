"""Echo request message tests."""
from pyof.v0x01.symmetric.echo_request import EchoRequest
from tests.test_struct import TestMsgDumpFile


class TestEchoRequest(TestMsgDumpFile):
    """Echo request message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_echo_request.dat'
    obj = EchoRequest(xid=0)
    min_size = 8
