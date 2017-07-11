"""Testing VendorHeader message."""
from pyof.v0x01.symmetric.vendor_header import VendorHeader
from tests.test_struct import TestMsgDumpFile


class TestVendorHeader(TestMsgDumpFile):
    """Vendor message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_vendor_header.dat'
    obj = VendorHeader(xid=4, vendor=128)
    min_size = 12
