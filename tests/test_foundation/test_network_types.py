"""Test Python-openflow network types."""
from pyof.foundation.basic_types import BinaryData
from pyof.foundation.network_types import GenericTLV, IPv4
from tests.test_struct import TestStructDump


class TestGenericTLV(TestStructDump):
    """Test the GenericTLV value data."""

    dump = b'\xfe\x04test'
    obj = GenericTLV(value=BinaryData(b'test'))


class TestIPV4(TestStructDump):
    """Test the IPV4 class."""

    dump = b'F(\x00 \x00\x00\x00\x00@\x11\x02' +\
        b'\xc5\xc0\xa8\x00\n\xac\x10\n\x1e1000testdata'
    obj = IPv4(dscp=10, ttl=64, protocol=17, source="192.168.0.10",
               destination="172.16.10.30", options=b'1000',
               data=b'testdata')

    def test_IPv4_checksum(self):
        """Test if the IPv4 checksum is being calculated correclty."""
        self.assertEqual(self._unpacked_dump.checksum, 709)
