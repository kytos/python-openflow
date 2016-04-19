import unittest

from ofp.v0x01.common import header as ofp_header


class TestHeader(unittest.TestCase):
    """Test the message Header"""

    def setUp(self):
        """Setup the TestHeader Class instantiating a HELLO header"""
        self.header = ofp_header.OFPHeader(ofp_header.OFPType.OFPT_HELLO,
                                           xid=1,
                                           length=0)

    def test_init_no_ofptype(self):
        """Tests the constructor without passing ofp_type
        This shouldn't pass (init fails)"""
        with self.assertRaises(TypeError):
            ofp_header.OFPHeader(xid=1, length=0)

    def test_init_no_xid(self):
        """Tests the constructor without passing the xid.
        This shouldn't pass (init fails)"""
        with self.assertRaises(TypeError):
            ofp_header.OFPHeader(length=0,
                                 ofp_type=ofp_header.OFPType.OFPT_HELLO)

    def test_init_no_length(self):
        """Tests the constructor without passing the length.
        This should pass."""
        self.assertIsInstance(ofp_header.OFPHeader(
            xid=1,
            ofp_type=ofp_header.OFPType.OFPT_HELLO), ofp_header.OFPHeader)

    def test_size(self):
        """Test the size of the header, always should be 8"""
        self.assertEqual(self.header.get_size(), 8)

    def test_pack(self):
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
