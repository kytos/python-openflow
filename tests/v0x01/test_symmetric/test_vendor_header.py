"""Testing VendorHeader message."""
from pyof.v0x01.symmetric.vendor_header import VendorHeader
from tests.test_struct import TestStruct


class TestVendorHeader(TestStruct):
    """Vendor message tests (also those in :class:`.TestDump`)."""

    def test_unpack(self):
        """Test unpack VendorHeader message."""
        message = b'My custom vendor extra data.'
        vendor_header = VendorHeader(xid=4, vendor=128,
                                     data=message)
        data = b'\x01\x04\x00(\x00\x00\x00\x04\x00\x00\x00\x80' + message
        self._test_unpack(vendor_header, bytes2unpack=data)
