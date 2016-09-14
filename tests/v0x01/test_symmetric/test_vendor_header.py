"""Testing VendorHeader message."""
import unittest

from pyof.v0x01.symmetric import vendor_header


class TestVendorHeader(unittest.TestCase):
    """Testing VendorHeader message."""

    def setUp(self):
        """Basic Test Setup."""
        self.message = vendor_header.VendorHeader(xid=4, vendor=1)

    def test_get_size(self):
        """[Symmetric/VendorHeader] - size 12."""
        self.assertEqual(self.message.get_size(), 12)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Symmetric/VendorHeader] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Symmetric/VendorHeader] - unpacking."""
        # TODO
        pass
