"""Echo reply message tests."""
from pyof.v0x04.symmetric.echo_reply import EchoReply
from tests.test_struct import TestStruct


class TestEchoReply(TestStruct):
    """Echo reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_echo_reply')
        super().set_raw_dump_object(EchoReply, xid=0)
        super().set_minimum_size(8)
