"""Hello message tests."""
from pyof.v0x01.symmetric.hello import Hello
from tests.test_struct import TestMsgDumpFile


class TestHello(TestMsgDumpFile):
    """Hello message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_hello.dat'
    obj = Hello(xid=1)
    min_size = 8
