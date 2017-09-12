"""Automate utils tests."""
import unittest

from pyof.utils import UnpackException, unpack, validate_packet
from pyof.v0x01.symmetric.hello import Hello as Hello_v0x01
from pyof.v0x04.symmetric.hello import Hello as Hello_v0x04


class TestUtils(unittest.TestCase):
    """Run tests to verify unpack independent of version."""

    def test_unpack_v0x01_packet(self):
        """Test if the package in version v0x01 is properly unpacked."""
        data = Hello_v0x01().pack()
        expected = unpack(data)
        self.assertEqual(expected.pack(), data)

    def test_unpack_v0x04_packet(self):
        """Test if the package in version v0x04 is properly unpacked."""
        data = Hello_v0x04().pack()
        expected = unpack(data)
        self.assertEqual(expected.pack(), data)

    def test_invalid_packet_with_version_more_then_128(self):
        """Test validate a invalid packet with version more than 128."""
        hello = Hello_v0x04()
        hello.header.version = 129

        self.assertRaises(UnpackException, validate_packet, hello.pack())

    def test_validate_packet_with_invalid_packets(self):
        """Test validate a invalid packet with invalid packets."""
        hello = Hello_v0x04()

        hello.header.version = 128
        self.assertRaises(UnpackException, validate_packet, hello.pack())

        hello.header.version = 0
        self.assertRaises(UnpackException, validate_packet, hello.pack())
