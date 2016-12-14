"""Testing Header structure."""
import os
import unittest
from unittest.mock import patch

from pyof.v0x01.common.header import Header, Type


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
        self.assertRaises(TypeError,
                          Header().pack())

    def test_pack(self):
        """[Common/Header] - packing Hello."""
        packed_header = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed_header)

    def test_unpack(self):
        """[Common/Header] - unpacking Hello."""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_hello.dat')
        f = open(filename, 'rb')
        self.message.unpack(f.read(8))

        self.assertEqual(self.message.length, 8)
        self.assertEqual(self.message.xid, 1)
        self.assertEqual(self.message.message_type, Type.OFPT_HELLO)
        self.assertEqual(self.message.version, 1)

        f.close()

    @patch('pyof.v0x01.common.header.randint')
    def test_random_xid(self, m):
        """Each Header instantiations without xid should call randint."""
        Header(), Header()  # noqa
        self.assertEqual(m.call_count, 2)
