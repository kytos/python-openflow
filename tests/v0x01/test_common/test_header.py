import unittest

from ofp.v0x01.common import header as of_header


class TestHeader(unittest.TestCase):
    """Test the message Header"""

    def setUp(self):
        """Setup the TestHeader Class instantiating a HELLO header"""
        self.header = of_header.OFPHeader(of_header.OFPType.OFPT_HELLO,
                                          xid=1,
                                          length=0)

    def test_size(self):
        """Test the size of the header, always should be 8"""
        self.assertEqual(self.header.get_size(), 8)

    def test_pack_empty(self):
        """Test the pack method for the an empty header"""
        self.assertRaises(TypeError,
                          self.header.pack())

    def test_pack_hello(self):
        """Test the pack method for the header
        Testing a header for type HELLO, length=0 and xid=1"""
        packet_header = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.header.pack(), packet_header)

    def test_unpack(self):
        """Test header unpacking.
        Should read a raw binary datapack, get the first 8 bytes and
        then unpack it as a header object."""
        # self.assertEqual(unpacked_header, self.header)
        pass
