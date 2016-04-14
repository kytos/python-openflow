import unittest

from ofp.v0x01.symmetric import vendor

class TestVendorHeader(unittest.TestCase):
    def test_get_size(self):
        vendor_header = vendor.VendorHeader(xid=4, vendor=1)
        self.assertEqual(vendor_header.get_size(), 8)

    def test_pack(self):
        vendor_header = vendor.VendorHeader(xid=4, vendor=1)
        vendor_header.pack()

    def test_unpack(self):
        pass
