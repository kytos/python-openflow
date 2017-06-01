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

    def test_IPv4_pack_unpack(self):
        """Test pack/unpack of IPv4 class."""
        packet = IPv4(ttl=64, protocol=17, source="192.168.0.1",
                      destination="172.16.200.132", data=b'testdata')
        packed = packet.pack()
        unpacked = IPv4()
        unpacked.unpack(packed)
        self.assertEqual(packed, unpacked.pack())
