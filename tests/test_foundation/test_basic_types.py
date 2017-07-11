"""Tests for Python-openflow BasicTypes."""
import unittest

from pyof.foundation import basic_types
from pyof.foundation.basic_types import BinaryData
from tests.test_struct import TestStructDump


class TestUBInt8_(unittest.TestCase):
    """Test UBInt8."""

    dump = b'\xff'
    obj = basic_types.UBInt32(2**8 - 1)
    min_size = 1


class TestUBInt16_(unittest.TestCase):
    """Test UBInt16."""

    dump = b'\xff\xff'
    obj = basic_types.UBInt32(2**16 - 1)
    min_size = 2


class TestUBInt32_(unittest.TestCase):
    """Test UBInt32."""

    dump = b'\xff\xff\xff\xff'
    obj = basic_types.UBInt32(2**32 - 1)
    min_size = 4


class TestChar_3(unittest.TestCase):
    """Test Char with length 3."""

    dump = b'fo\x00'
    obj = basic_types.Char('foo', length=3)


class TestChar_5(unittest.TestCase):
    """Test Char with length 5."""

    dump = b'foo\x00\x00'
    obj = basic_types.Char('foo', length=5)


class TestHWAddress_default(TestStructDump):
    """Test HWAddress default value."""

    dump = b'\x00\x00\x00\x00\x00\x00'
    obj = basic_types.HWAddress()


class TestHWAddress_mac(TestStructDump):
    """Test HWAddress mac value."""

    mac = '00:00:00:00:00:00'
    dump = b'\x00\x00\x00\x00\x00\x00'
    obj = basic_types.HWAddress(mac)

    def test_address_value(self):
        """Test HWAddress mac value."""
        self.assertEqual(self.obj.value, self.mac)


class TestHWAddress_random(TestHWAddress_mac):
    """Test HWAddress mac value 0a:d3:98:a5:30:47."""

    mac = '0a:d3:98:a5:30:47'
    dump = b'\x0a\xd3\x98\xa5\x30\x47'
    obj = basic_types.HWAddress(mac)


class TestIPAddress_netmask(TestStructDump):
    """Test IPAddress and its default netmask value."""

    dump = b'\xc0\xa8\x00\x01'
    obj = basic_types.IPAddress('192.168.0.1')
    netmask = 32

    def test_netmask(self):
        """Test IPAddress netmask value."""
        self.assertEqual(self.obj.netmask, self.netmask)


class TestIPAddress_nonetmask(TestIPAddress_netmask):
    """Test IPAdress and netmask value 16."""

    dump = b'\xc0\xa8\x00\x01'
    obj = basic_types.IPAddress('192.168.0.1/16')
    netmask = 16


class TestBinaryData_empty(TestStructDump):
    """Test empty BinaryData."""

    dump = b''
    obj = BinaryData()
    min_size = 0


class TestBinaryData_bytes(TestStructDump):
    """Test 'bytes' BinaryData."""

    dump = b'bytes'
    obj = BinaryData(b'bytes')


class TestUBInt8(unittest.TestCase):
    """Test of UBInt8 BasicType."""

    def setUp(self):
        """Basic test setup."""
        self.ubint8 = basic_types.UBInt8()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt8] - size 1."""
        self.assertEqual(self.ubint8.get_size(), 1)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt8] - packing."""
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt8] - unpacking."""
        pass


class TestUBInt16(unittest.TestCase):
    """Test of UBInt16 BasicType."""

    def setUp(self):
        """Basic test setup."""
        self.ubint16 = basic_types.UBInt16()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt16] - size 2."""
        self.assertEqual(self.ubint16.get_size(), 2)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt16] - packing."""
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt16] - unpacking."""
        pass


class TestUBInt32(unittest.TestCase):
    """Test of UBInt32 BasicType."""

    def setUp(self):
        """Basic test setup."""
        self.ubint32 = basic_types.UBInt32()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt32] - size 4."""
        self.assertEqual(self.ubint32.get_size(), 4)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt32] - packing."""
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt32] - unpacking."""
        pass


class TestChar(unittest.TestCase):
    """Test of Char BasicType."""

    def setUp(self):
        """Basic test setup."""
        self.char1 = basic_types.Char('foo', length=3)
        self.char2 = basic_types.Char('foo', length=5)

    def test_get_size(self):
        """[Foundation/BasicTypes/Char] - get_size."""
        self.assertEqual(self.char1.get_size(), 3)
        self.assertEqual(self.char2.get_size(), 5)

    def test_pack(self):
        """[Foundation/BasicTypes/Char] - packing."""
        self.assertEqual(self.char1.pack(), b'fo\x00')
        self.assertEqual(self.char2.pack(), b'foo\x00\x00')

    def test_unpack(self):
        """[Foundation/BasicTypes/Char] - unpacking."""
        char1 = basic_types.Char(length=3)
        char2 = basic_types.Char(length=5)
        char1.unpack(b'fo\x00')
        char2.unpack(b'foo\x00\x00')

        self.assertEqual(char1.value, 'fo')
        self.assertEqual(char2.value, 'foo')


class TestHWaddress(unittest.TestCase):
    """Test of HWAddress BasicType."""

    def test_unpack_packed(self):
        """Testing unpack of packed HWAddress."""
        mac = '0a:d3:98:a5:30:47'
        hw_addr = basic_types.HWAddress(mac)
        packed = hw_addr.pack()
        unpacked = basic_types.HWAddress()
        unpacked.unpack(packed)
        self.assertEqual(mac, unpacked.value)

    def test_default_value(self):
        """Testing default_value for HWAddress."""
        mac = '00:00:00:00:00:00'
        hw_addr = basic_types.HWAddress()
        packed = hw_addr.pack()
        unpacked = basic_types.HWAddress()
        unpacked.unpack(packed)
        self.assertEqual(mac, unpacked.value)


class TestIPAddress(unittest.TestCase):
    """Test of IPAddress BasicType."""

    def test_unpack_packed(self):
        """Test unpacking of packed IPAddress."""
        ip_addr = basic_types.IPAddress('192.168.0.1')
        packed = ip_addr.pack()
        unpacked = basic_types.IPAddress()
        unpacked.unpack(packed)
        self.assertEqual(ip_addr.value, unpacked.value)

    def test_unpack_packed_with_netmask(self):
        """Testing unpack of packed IPAddress with netmask."""
        ip_addr = basic_types.IPAddress('192.168.0.1/16')
        packed = ip_addr.pack()
        unpacked = basic_types.IPAddress()
        unpacked.unpack(packed)
        self.assertEqual(ip_addr.value, unpacked.value)

    def test_netmask(self):
        """Testing get netmask from IPAddress."""
        ip_addr = basic_types.IPAddress('192.168.0.1/24')
        self.assertEqual(ip_addr.netmask, 24)
        ip_addr = basic_types.IPAddress('192.168.0.1/16')
        self.assertEqual(ip_addr.netmask, 16)
        ip_addr = basic_types.IPAddress('192.168.0.1')
        self.assertEqual(ip_addr.netmask, 32)

    def test_max_prefix(self):
        """Testing get max_prefix from IPAddress."""
        ip_addr = basic_types.IPAddress()
        self.assertEqual(ip_addr.max_prefix, 32)
        ip_addr = basic_types.IPAddress('192.168.0.35/16')
        self.assertEqual(ip_addr.max_prefix, 32)

    def test_get_size(self):
        """Testing get_size from IPAddress."""
        ip_addr = basic_types.IPAddress('192.168.0.1/24')
        self.assertEqual(ip_addr.get_size(), 4)


class TestBinaryData(unittest.TestCase):
    """Test Binary data type."""

    def test_default_value(self):
        """Default packed value should be an empty byte."""
        expected = b''
        actual = BinaryData().pack()
        self.assertEqual(expected, actual)

    def test_pack_bytes(self):
        """Test packing some bytes."""
        expected = b'forty two'
        actual = BinaryData(expected).pack()
        self.assertEqual(expected, actual)

    def test_pack_empty_bytes(self):
        """Test packing empty bytes."""
        expected = b''
        actual = BinaryData(expected).pack()
        self.assertEqual(expected, actual)

    def test_unexpected_value(self):
        """Should raise ValueError if constructor value is not bytes."""
        self.assertRaises(ValueError, BinaryData, "can't be string")

    def test_unexpected_value_as_parameter(self):
        """Should raise ValueError if pack value is not bytes."""
        self.assertRaises(ValueError, BinaryData().pack, "can't be string")
