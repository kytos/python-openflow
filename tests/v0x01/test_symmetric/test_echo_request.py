"""Echo request message tests."""
from pyof.v0x01.symmetric.echo_request import EchoRequest
from tests.test_struct import TestStruct


class TestEchoRequest(TestStruct):
    """Echo request message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_echo_request')
        super().set_raw_dump_object(EchoRequest, xid=0)
        super().set_minimum_size(8)
