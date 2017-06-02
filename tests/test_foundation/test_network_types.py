"""Test Python-openflow network types."""
import unittest

from pyof.foundation.basic_types import BinaryData
from pyof.foundation.network_types import GenericTLV, IPv4


class TestNetworkTypes(unittest.TestCase):
    """Reproduce bugs found."""

    def test_GenTLV_value_unpack(self):
        """Value attribute should be the same after unpacking."""
        value = BinaryData(b'test')
        tlv = GenericTLV(value=value)
        tlv_unpacked = GenericTLV()
        tlv_unpacked.unpack(tlv.pack())
        self.assertEqual(tlv.value.value, tlv_unpacked.value.value)


class TestIPv4(unittest.TestCase):
    """Test IPv4 packets."""

    def test_IPv4_pack(self):
        """Test pack/unpack of IPv4 class."""
        packet = IPv4(dscp=10, ttl=64, protocol=17, source="192.168.0.10",
                      destination="172.16.10.30", options=b'1000',
                      data=b'testdata')
        packed = packet.pack()
        expected = b'F(\x00 \x00\x00\x00\x00@\x11\x02'
        expected += b'\xc5\xc0\xa8\x00\n\xac\x10\n\x1e1000testdata'
        self.assertEqual(packed, expected)

    def test_IPv4_unpack(self):
        """Test unpack of IPv4 binary packet."""
        raw = b'FP\x00$\x00\x00\x00\x00\x80\x06W'
        raw += b'\xf4\n\x9aN\x81\xc0\xa8\xc7\xcc1000somemoredata'
        expected = IPv4(dscp=20, ttl=128, protocol=6, source="10.154.78.129",
                        destination="192.168.199.204", options=b'1000',
                        data=b'somemoredata')
        expected.pack()
        unpacked = IPv4()
        unpacked.unpack(raw)
        self.assertEqual(unpacked, expected)

    def test_IPv4_size(self):
        """Test Header size for IPv4 packet."""
        packet = IPv4()
        packet.pack()
        self.assertEqual(20, packet.get_size())
        self.assertEqual(20, packet.length)
        self.assertEqual(20, packet.ihl * 4)

    def test_IPv4_checksum(self):
        """Test if the IPv4 checksum is being calculated correclty."""
        packet = IPv4(dscp=10, ttl=64, protocol=17, source="192.168.0.10",
                      destination="172.16.10.30", options=b'1000',
                      data=b'testdata')
        packet.pack()
        self.assertEqual(packet.checksum, 709)
