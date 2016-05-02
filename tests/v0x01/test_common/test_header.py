import unittest

from ofp.v0x01.common import header as of_header


class TestHeader(unittest.TestCase):
    """Test the message Header"""

    def setUp(self):
        """Setup the TestHeader Class instantiating a HELLO header"""
        self.message = of_header.Header()
        self.message.ofp_type = of_header.Type.OFPT_HELLO
        self.message.xid = 1
        self.message.length = 0

    def test_size(self):
        """[Common/Header] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.expectedFailure
    def test_pack_empty(self):
        """[Common/Header] - packing empty header"""
        self.assertRaises(TypeError,
                          of_header.Header().pack())

    def test_pack(self):
        """[Common/Header] - packing Hello"""
        packed_header = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_header)

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/Header] - unpacking Hello"""
        # TODO
        pass
