"""Tests header structure of v0x04."""
import os
import unittest

from pyof.v0x04.common.header import Header, Type


class TestHeader(unittest.TestCase):
    """Test the message Header."""

    def setUp(self):
        """Setup the TestHeader Class instantiating a HELLO header."""
        self.message = Header()
        self.message.message_type = Type.OFPT_HELLO
        self.message.xid = 1
        self.message.length = 0

    def test_size(self):
        """[Common/Header] - size 8."""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.expectedFailure
    def test_pack_empty(self):
        """[Common/Header] - packing empty header."""
        self.assertRaises(TypeError, Header().pack())

    def test_pack(self):
        """[Common/Header] - packing Hello."""
        packed_header = b'\x04\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_header)

    def test_unpack(self):
        """[Common/Header] - unpacking Hello."""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x04/ofpt_hello.dat')
        try:
            f = open(filename, 'rb')
            self.message.unpack(f.read(8))

            self.assertEqual(self.message.length, 8)
            self.assertEqual(self.message.xid, 1)
            self.assertEqual(self.message.message_type, Type.OFPT_HELLO)
            self.assertEqual(self.message.version, 0x04)

            f.close()
        except FileNotFoundError:
            raise self.skipTest('There is no raw dump file for this test')
