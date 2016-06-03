import unittest

import os
from pyof.v0x01.common import header as of_header


class TestHeader(unittest.TestCase):
    """Test the message Header"""

    def setUp(self):
        """Setup the TestHeader Class instantiating a HELLO header"""
        self.message = of_header.Header()
        self.message.message_type = of_header.Type.OFPT_HELLO
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

    def test_unpack(self):
        """[Common/Header] - unpacking Hello"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_hello.dat')
        f = open(filename,'rb')
        self.message.unpack(f.read(8))

        self.assertEqual(self.message.length, 8)
        self.assertEqual(self.message.xid, 1)
        self.assertEqual(self.message.message_type, of_header.Type.OFPT_HELLO)
        self.assertEqual(self.message.version, 1)

        f.close()
