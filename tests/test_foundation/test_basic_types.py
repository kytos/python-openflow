"""Tests for Python-openflow BasicTypes."""
import unittest

from pyof.foundation import basic_types
from pyof.foundation.basic_types import BinaryData
from tests.test_struct import TestStructDump


class TestUBInt8(TestStructDump):
    """Test UBInt8."""

    dump = b'\xff'
    obj = basic_types.UBInt8(2**8 - 1)
    min_size = 1


class TestUBInt16(TestStructDump):
    """Test UBInt16."""

    dump = b'\xff\xff'
    obj = basic_types.UBInt16(2**16 - 1)
    min_size = 2


class TestUBInt32(TestStructDump):
    """Test UBInt32."""

    dump = b'\xff\xff\xff\xff'
    obj = basic_types.UBInt32(2**32 - 1)
    min_size = 4


class TestChar3(TestStructDump):
    """Test Char with length 3."""

    dump = b'fo\x00'
    obj = basic_types.Char('foo', length=3)


class TestChar5(TestStructDump):
    """Test Char with length 5."""

    dump = b'foo\x00\x00'
    obj = basic_types.Char('foo', length=5)


class TestHWAddressDefault(TestStructDump):
    """Test HWAddress default value."""

    dump = b'\x00\x00\x00\x00\x00\x00'
    obj = basic_types.HWAddress()


class TestHWAddressMac(TestStructDump):
    """Test HWAddress mac value."""

    mac = '00:00:00:00:00:00'
    dump = b'\x00\x00\x00\x00\x00\x00'
    obj = basic_types.HWAddress(mac)

    def test_address_value(self):
        """Test HWAddress mac value."""
        self.assertEqual(self.obj.value, self.mac)


class TestHWAddressRandom(TestHWAddressMac):
    """Test HWAddress mac value 0a:d3:98:a5:30:47."""

    mac = '0a:d3:98:a5:30:47'
    dump = b'\x0a\xd3\x98\xa5\x30\x47'
    obj = basic_types.HWAddress(mac)


class TestIPAddressNetmask(TestStructDump):
    """Test IPAddress and its default netmask value."""

    dump = b'\xc0\xa8\x00\x01'
    obj = basic_types.IPAddress('192.168.0.1')
    netmask = 32

    def test_netmask(self):
        """Test IPAddress netmask value."""
        self.assertEqual(self.obj.netmask, self.netmask)


class TestIPAddressNoNetmask(TestIPAddressNetmask):
    """Test IPAdress and netmask value 16."""

    dump = b'\xc0\xa8\x00\x01'
    obj = basic_types.IPAddress('192.168.0.1/16')
    netmask = 16


class TestBinaryDataEmpty(TestStructDump):
    """Test empty BinaryData."""

    dump = b''
    obj = BinaryData()
    min_size = 0


class TestBinaryDataBytes(TestStructDump):
    """Test 'bytes' BinaryData."""

    dump = b'bytes'
    obj = BinaryData(b'bytes')


class TestIPAddress(unittest.TestCase):
    """Test of IPAddress BasicType max_prefix."""

    def test_max_prefix(self):
        """Testing get max_prefix from IPAddress."""
        ip_addr = basic_types.IPAddress()
        self.assertEqual(ip_addr.max_prefix, 32)
        ip_addr = basic_types.IPAddress('192.168.0.35/16')
        self.assertEqual(ip_addr.max_prefix, 32)


class TestBinaryData(unittest.TestCase):
    """Test Binary data type cannot accept string."""

    def test_unexpected_value(self):
        """Should raise ValueError if constructor value is not bytes."""
        self.assertRaises(ValueError, BinaryData, "can't be string")

    def test_unexpected_value_as_parameter(self):
        """Should raise ValueError if pack value is not bytes."""
        self.assertRaises(ValueError, BinaryData().pack, "can't be string")
