"""Test OXM-related implementations."""
from unittest import TestCase

from pyof.foundation.exceptions import PackException, UnpackException
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)


class TestMatch(TestCase):
    """Test Match class."""

    tlv1 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                  oxm_field=OxmOfbMatchField.OFPXMT_OFB_IN_PHY_PORT,
                  oxm_hasmask=True, oxm_value=b'abc')
    tlv2 = OxmTLV(oxm_class=OxmClass.OFPXMC_EXPERIMENTER,
                  oxm_field=OxmOfbMatchField.OFPXMT_OFB_METADATA,
                  oxm_hasmask=False, oxm_value=b'abcdef')
    match = Match(match_type=MatchType.OFPMT_OXM,
                  oxm_match_fields=[tlv1, tlv2])

    def test_unpacked_pack(self):
        """Pack and then unpack the result and check for equality.

        Use two TLVs to also test match-field list packing/unpacking.
        """
        unpacked = Match()
        unpacked.unpack(self.match.pack())
        self.assertEqual(self.match, unpacked)

    def test_pack_other_instance(self):
        """Test packing another Match instance by using the value argument."""
        expected = self.match.pack()
        valued_pack = Match().pack(self.match)
        self.assertEqual(expected, valued_pack)


class TestOxmTLV(TestCase):
    """Test OXM TLV pack and unpack."""

    def setUp(self):
        """Instantiate an OXM TLV struct."""
        self.tlv = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                          oxm_field=OxmOfbMatchField.OFPXMT_OFB_IN_PHY_PORT,
                          oxm_hasmask=False, oxm_value=b'')

    def test_different_class_types(self):
        """Pack, unpack the result and assert the values are equal."""
        for oxm_class in (OxmClass.OFPXMC_OPENFLOW_BASIC,
                          OxmClass.OFPXMC_EXPERIMENTER):
            self.tlv.oxm_class = oxm_class
            unpacked = self._create_from_pack()
            self.assertEqual(oxm_class, unpacked.oxm_class)

    def test_different_fields(self):
        """Pack, unpack the result and assert the values are equal."""
        for oxm_field in (OxmOfbMatchField.OFPXMT_OFB_IN_PORT,
                          OxmOfbMatchField.OFPXMT_OFB_IPV6_EXTHDR):
            self.tlv.oxm_field = oxm_field
            unpacked = self._create_from_pack()
            self.assertEqual(oxm_field, unpacked.oxm_field)

    def test_hasmask_bit(self):
        """Pack, unpack the result and assert the values are equal."""
        for oxm_hasmask in True, False:
            self.tlv.oxm_hasmask = oxm_hasmask
            unpacked = self._create_from_pack()
            self.assertEqual(oxm_hasmask, unpacked.oxm_hasmask)

    def test_different_values(self):
        """Pack, unpack the result and assert the values are equal."""
        for oxm_value in b'', b'abc':
            self.tlv.oxm_value = oxm_value
            unpacked = self._create_from_pack()
            self.assertEqual(oxm_value, unpacked.oxm_value)

    def _create_from_pack(self):
        """Return a new instance by unpacking self.tlv.pack()."""
        unpacked = OxmTLV()
        unpacked.unpack(self.tlv.pack())
        return unpacked

    def test_pack_overflowed_field(self):
        """Raise PackException if field is bigger than 7 bit."""
        self.tlv.oxm_class = OxmClass.OFPXMC_EXPERIMENTER
        self.tlv.oxm_field = 2**7
        with self.assertRaises(PackException):
            self.tlv.pack()

    def test_pack_invalid_field(self):
        """Raise PackException if field is invalid for a class.

        Example: field 42 is invalid for oxm_class OFPXMC_OPENFLOW_BASIC.
        """
        self.tlv.oxm_class = OxmClass.OFPXMC_OPENFLOW_BASIC
        self.tlv.oxm_field = 42
        with self.assertRaises(PackException):
            self.tlv.pack()

    def test_unpack_invalid_field(self):
        """Raise UnpackException if field is invalid for a class.

        Example: field 42 is invalid for oxm_class OFPXMC_OPENFLOW_BASIC.
        """
        field42 = b'\x80\x00T\x00'
        tlv = OxmTLV()
        with self.assertRaises(UnpackException):
            tlv.unpack(field42)

    def test_max_field_value(self):
        """Use all bits of oxm_field."""
        self.tlv.oxm_class = OxmClass.OFPXMC_EXPERIMENTER
        self.tlv.oxm_field = 127
        unpacked = OxmTLV()
        unpacked.unpack(self.tlv.pack())
        self.assertEqual(self.tlv, unpacked)
