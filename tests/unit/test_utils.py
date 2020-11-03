"""Automate utils tests."""
import unittest

from pyof import v0x01, v0x04
from pyof.utils import (is_ofbac_bad_out_port, get_port_config_for_version,
                        UnpackException, unpack, UnsupportedVersionException,
                        validate_packet)
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

    def test_is_ofbac_bad_out_port_with_valid_code(self):
        """Test is_ofbac_bad_out_port using a valid code."""
        code = 4

        self.assertEqual(is_ofbac_bad_out_port(code), True)

    def test_is_ofbac_bad_out_port_with_invalid_code(self):
        """Test is_ofbac_bad_out_port using a valid code."""
        code = 0

        self.assertEqual(is_ofbac_bad_out_port(code), False)

    def test_success_get_port_config_for_version(self):
        """Test get_port_config_for_version success cases."""
        port_config_v0x01 = v0x01.common.phy_port.PortConfig.OFPPC_NO_FWD
        port_config_v0x04 = v0x04.common.port.PortConfig.OFPPC_NO_FWD

        self.assertEqual(get_port_config_for_version(0x01), port_config_v0x01)
        self.assertEqual(get_port_config_for_version(0x04), port_config_v0x04)

    def test_fail_get_port_config_for_version(self):
        """Test get_port_config_for_version success cases."""

        self.assertRaises(UnsupportedVersionException,
                          get_port_config_for_version, 0x00)
