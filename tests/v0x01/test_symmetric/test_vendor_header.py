"""Testing VendorHeader message."""
from pyof.v0x01.symmetric.vendor_header import VendorHeader
from tests.test_struct import TestStruct


class TestVendorHeader(TestStruct):
    """Vendor message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_vendor_header')
        super().set_raw_dump_object(VendorHeader, xid=4, vendor=128)
        super().set_minimum_size(12)
