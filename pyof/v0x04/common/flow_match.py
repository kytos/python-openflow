"""Match strucutre and related enums.

An OpenFlow match is composed of a flow match header and a sequence of zero or
more flow match fields.
"""
# System imports
from enum import Enum, IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, CustomTLV_24_8, FixedTypeList, Pad, UBInt8, UBInt16, UBInt32)

# Third-party imports


__all__ = ('Ipv6ExtHdrFlags', 'Match', 'OxmOfbMatchField', 'MatchType',
           'OxmExperimenterHeader', 'OxmMatchFields', 'VlanId')


class Ipv6ExtHdrFlags(Enum):
    """Bit definitions for IPv6 Extension Header pseudo-field."""

    #: "No next header" encountered.
    OFPIEH_NONEXT = 1 << 0
    #: Encrypted Sec Payload header present.
    OFPIEH_ESP = 1 << 1
    #: Authentication header present.
    OFPIEH_AUTH = 1 << 2
    #: 1 or 2 dest headers present.
    OFPIEH_DEST = 1 << 3
    #: Fragment header present.
    OFPIEH_FRAG = 1 << 4
    #: Router header present.
    OFPIEH_ROUTER = 1 << 5
    #: Hop-by-hop header present.
    OFPIEH_HOP = 1 << 6
    #: Unexpected repeats encountered.
    OFPIEH_UNREP = 1 << 7
    #: Unexpected sequencing encountered.
    OFPIEH_UNSEQ = 1 << 8


class OxmOfbMatchField(IntEnum):
    """OXM Flow match field types for OpenFlow basic class.

    A switch is not required to support all match field types, just those
    listed in the Table 10. Those required match fields don’t need to be
    implemented in the same table lookup. The controller can query the switch
    about which other fields it supports.
    """

    #: Switch input port.
    OFPXMT_OFB_IN_PORT = 0
    #: Switch physical input port.
    OFPXMT_OFB_IN_PHY_PORT = 1
    #: Metadata passed between tables.
    OFPXMT_OFB_METADATA = 2
    #: Ethernet destination address.
    OFPXMT_OFB_ETH_DST = 3
    #: Ethernet source address.
    OFPXMT_OFB_ETH_SRC = 4
    #: Ethernet frame type.
    OFPXMT_OFB_ETH_TYPE = 5
    #: VLAN id.
    OFPXMT_OFB_VLAN_VID = 6
    #: VLAN priority.
    OFPXMT_OFB_VLAN_PCP = 7
    #: IP DSCP (6 bits in ToS field).
    OFPXMT_OFB_IP_DSCP = 8
    #: IP ECN (2 bits in ToS field).
    OFPXMT_OFB_IP_ECN = 9
    #: IP protocol.
    OFPXMT_OFB_IP_PROTO = 10
    #: IPv4 source address.
    OFPXMT_OFB_IPV4_SRC = 11
    #: IPv4 destination address.
    OFPXMT_OFB_IPV4_DST = 12
    #: TCP source port.
    OFPXMT_OFB_TCP_SRC = 13
    #: TCP destination port.
    OFPXMT_OFB_TCP_DST = 14
    #: UDP source port.
    OFPXMT_OFB_UDP_SRC = 15
    #: UDP destination port.
    OFPXMT_OFB_UDP_DST = 16
    #: SCTP source port.
    OFPXMT_OFB_SCTP_SRC = 17
    #: SCTP destination port.
    OFPXMT_OFB_SCTP_DST = 18
    #: ICMP type.
    OFPXMT_OFB_ICMPV4_TYPE = 19
    #: ICMP code.
    OFPXMT_OFB_ICMPV4_CODE = 20
    #: ARP opcode.
    OFPXMT_OFB_ARP_OP = 21
    #: ARP source IPv4 address.
    OFPXMT_OFB_ARP_SPA = 22
    #: ARP target IPv4 address.
    OFPXMT_OFB_ARP_TPA = 23
    #: ARP source hardware address.
    OFPXMT_OFB_ARP_SHA = 24
    #: ARP target hardware address.
    OFPXMT_OFB_ARP_THA = 25
    #: IPv6 source address.
    OFPXMT_OFB_IPV6_SRC = 26
    #: IPv6 destination address.
    OFPXMT_OFB_IPV6_DST = 27
    #: IPv6 Flow Label
    OFPXMT_OFB_IPV6_FLABEL = 28
    #: ICMPv6 type.
    OFPXMT_OFB_ICMPV6_TYPE = 29
    #: ICMPv6 code.
    OFPXMT_OFB_ICMPV6_CODE = 30
    #: Target address for ND.
    OFPXMT_OFB_IPV6_ND_TARGET = 31
    #: Source link-layer for ND.
    OFPXMT_OFB_IPV6_ND_SLL = 32
    #: Target link-layer for ND.
    OFPXMT_OFB_IPV6_ND_TLL = 33
    #: MPLS label.
    OFPXMT_OFB_MPLS_LABEL = 34
    #: MPLS TC.
    OFPXMT_OFB_MPLS_TC = 35
    #: MPLS BoS bit.
    OFPXMT_OFP_MPLS_BOS = 36
    #: PBB I-SID.
    OFPXMT_OFB_PBB_ISID = 37
    #: Logical Port Metadata.
    OFPXMT_OFB_TUNNEL_ID = 38
    #: IPv6 Extension Header pseudo-field
    OFPXMT_OFB_IPV6_EXTHDR = 39


class MatchType(IntEnum):
    """Indicates the match structure in use.

    The match type is placed in the type field at the beginning of all match
    structures. The "OpenFlow Extensible Match" type corresponds to OXM TLV
    format described below and must be supported by all OpenFlow switches.
    Extensions that define other match types may be published on the ONF wiki.
    Support for extensions is optional
    """

    #: Deprecated
    OFPMT_STANDARD = 0
    #: OpenFlow Extensible Match
    OFPMT_OXM = 1


class OxmClass(IntEnum):
    """OpenFlow Extensible Match (OXM) Class IDs.

    The high order bit differentiate reserved classes from member classes.
    Classes 0x0000 to 0x7FFF are member classes, allocated by ONF.
    Classes 0x8000 to 0xFFFE are reserved classes, reserved for
    standardisation.
    """

    #: Backward compatibility with NXM
    OFPXMC_NXM_0 = 0x0000
    #: Backward compatibility with NXM
    OFPXMC_NXM_1 = 0x0001
    #: Basic class for OpenFlow
    OFPXMC_OPENFLOW_BASIC = 0x8000
    #: Experimenter class
    OFPXMC_EXPERIMENTER = 0xFFFF


class VlanId(IntEnum):
    """Indicates conditions of the Vlan.

    The VLAN id is 12-bits, so we can use the entire 16 bits to indicate
    special conditions.
    """

    #: Bit that indicate that a VLAN id is set.
    OFPVID_PRESENT = 0x1000
    #: No VLAN id was set
    OFPVID_NONE = 0x0000


# Classes

class OxmType(GenericStruct):
    """Oxm TLV `type` metafield.

    OxmType is defined by the combination of a OxmClass and a OxmField,

    Args:
        oxm_class (:class:`OxmClass`, int): The oxm TLV defined class.
        oxm_field (:class:`OxmOfbMatchField`, Oxm*MatchField, int): the oxm
        TLV defined field of the correspondent class
    """

    oxm_class = UBInt16(enum_ref=OxmClass)
    oxm_field = UBInt8()

    def __init__(self, oxm_class, oxm_field):
        super().__init__()
        cls = type(self)
        self.oxm_class = type(cls.oxm_class)(oxm_class)
        self.oxm_field = oxm_field


class OxmTLV(GenericStruct):
    """Oxm (Openflow Extensible Match) TLV.

    Args:
        oxm_class (:class:`OxmClass`, int): The oxm TLV defined class.
        oxm_field (:class:`OxmOfbMatchField`, Oxm*MatchField, int): the oxm
            TLV defined field of the correspondent oxm_class.
        oxm_hasmask (bool):
        oxm_value (:class:`BinaryData`, bytes):
    """

    oxm_class = UBInt16(enum_ref=OxmClass)
    oxm_field = UBInt8()
    oxm_hasmask = UBInt8()
    oxm_length = UBInt8()
    oxm_value = BinaryData()

    def __init__(self, oxm_class=None, oxm_field=None,
                 oxm_hasmask=None, oxm_value=None):
        super().__init__()
        self.oxm_class = oxm_class
        self.oxm_field = oxm_field
        self.oxm_hasmask = oxm_hasmask if oxm_hasmask else 0
        self.oxm_length = None
        self.oxm_value = oxm_value
        self.tlv_class = CustomTLV_24_8

    def unpack(self, buff, offset=0):
        """Unpack the buffer into a OxmTLV.

        Args:
            buff (bytes): The binary data to be unpacked.
            offset (int): If we need to shift the beginning of the data.
        """
        tlv = self.tlv_class()
        tlv.unpack(buff, offset)
        # print('tlv unpack values:')
        # print(type(tlv.tlv_type), tlv.tlv_type)
        # print(type(tlv.tlv_length), tlv.tlv_length)
        # print(type(tlv.tlv_value), tlv.tlv_value)
        self.oxm_class = tlv.tlv_type >> 8
        self.oxm_field = (tlv.tlv_type & 0xFF) >> 1
        self.oxm_hasmask = tlv.tlv_type & 1
        self.oxm_length = tlv.tlv_length
        self.oxm_value = tlv.tlv_value

    def _pack(self):
        tlv_type = ((self.oxm_class << 8) +
                    (self.oxm_field << 1) +
                    self.oxm_hasmask)

        tlv_value = self.oxm_value
        tlv = self.tlv_class(tlv_type, tlv_value)
        return tlv._pack()   # noqa

    def _get_size(self):
        size = super()._get_size() - 1
        return size


class OxmMatchFields(FixedTypeList):
    """Generic Openflow EXtensible Match header.

    Abstract class that can be instanciated as Match or OxmExperimenterHeader.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (OxmHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=OxmTLV, items=items)


class Match(GenericStruct):
    """Describes the flow match header structure.

    These are the fields to match against flows.

    The :attr:`~match_type` field is set to :attr:`~MatchType.OFPMT_OXM` and
    :attr:`length` field is set to the actual length of match structure
    including all match fields. The payload of the OpenFlow match is a set of
    OXM Flow match fields.
    """

    #: One of OFPMT_*
    match_type = UBInt16(enum_ref=MatchType)
    #: Length of Match (excluding padding)
    length = UBInt16()
    oxm_match_fields = OxmMatchFields()

    def __init__(self, match_type=None, oxm_match_fields=None):
        """Describe the flow match header structure.

        Args:
            match_type (MatchType): One of OFPMT_* (MatchType) items.
            length (int): Length of Match (excluding padding) followed by
                          Exactly (length - 4) (possibly 0) bytes containing
                          OXM TLVs, then exactly ((length + 7)/8*8 - length)
                          (between 0 and 7) bytes of all-zero bytes.
            oxm_fields (OxmMatchFields): Sample description.
        """
        super().__init__()
        self.match_type = match_type
        self.oxm_match_fields = oxm_match_fields
        self._update_match_length()

    def _update_match_length(self):
        self.length = super()._get_size()

    def _pack(self):
        self._update_match_length()
        packet = super()._pack()
        super_size = len(packet)
        lacking_bytes = (8 - (super_size % 8)) % 8
        if lacking_bytes != 0:
            packet += Pad(lacking_bytes).pack()
        return packet

    def _get_size(self):
        super_size = super()._get_size()
        return super_size + (8 - (super_size % 8)) % 8

    def unpack(self, buff, offset=0):
        """Unpack bytes buffer into this Instance."""
        begin = offset
        for name, value in list(self.get_class_attributes())[:-1]:
            size = self._unpack_attribute(name, value, buff, begin)
            begin += size
        self._unpack_attribute('oxm_match_fields', type(self).oxm_match_fields,
                               buff[:offset + self.length],
                               begin)


class OxmExperimenterHeader(GenericStruct):
    """Header for OXM experimenter match fields."""

    #: oxm_class = OFPXMC_EXPERIMENTER
    oxm_header = UBInt32(OxmClass.OFPXMC_EXPERIMENTER,
                         enum_ref=OxmClass)
    #: Experimenter ID which takes the same form as in struct
    #:     ofp_experimenter_header
    experimenter = UBInt32()

    def __init__(self, experimenter=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            experimenter (int): Experimenter ID which takes the same form as
              in struct ofp_experimenter_header
        """
        super().__init__()
        self.experimenter = experimenter


class ListOfOxmHeader(FixedTypeList):
    """List of Openflow EXtensible Match header instances.

    Represented by instances of OxmHeader.
    """

    def __init__(self, items=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            items (OxmHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=OxmTLV, items=items)
