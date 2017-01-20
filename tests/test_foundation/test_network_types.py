"""Test Python-openflow network types."""
import unittest

from pyof.foundation.basic_types import BinaryData
from pyof.foundation.network_types import GenericTLV


class TestNetworkTypes(unittest.TestCase):
    """Reproduce bugs found."""

    def test_GenTLV_value_unpack(self):
        """Value attribute should be the same after unpacking."""
        value = BinaryData(b'test')
        tlv = GenericTLV(value=value)
        tlv_unpacked = GenericTLV()
        tlv_unpacked.unpack(tlv.pack())
        self.assertEqual(tlv.value.value, tlv_unpacked.value.value)
