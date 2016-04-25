import unittest

from ofp.v0x01.symmetric import vendor_header


class TestVendorHeader(unittest.TestCase):
    def setUp(self):
        self.message = vendor.VendorHeader(xid=4, vendor=1)

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 12)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
