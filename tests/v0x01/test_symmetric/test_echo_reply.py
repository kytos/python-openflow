"""Echo reply message tests."""
from pyof.v0x01.symmetric.echo_reply import EchoReply
from tests.test_struct import TestMsgDumpFile


class TestEchoReply(TestMsgDumpFile):
    """Echo reply message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_echo_reply.dat'
    obj = EchoReply(xid=0)
    min_size = 8
