"""Hello message tests."""
from pyof.v0x04.symmetric.hello import Hello
from tests.test_struct import TestStruct


class TestHello(TestStruct):
    """Hello message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_hello')
        super().set_raw_dump_object(Hello, xid=1)
        super().set_minimum_size(8)
