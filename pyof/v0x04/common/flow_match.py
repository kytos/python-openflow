"""Match strucutre and related enums.

An OpenFlow match is composed of a flow match header and a sequence of zero or
more flow match fields.
"""
# System imports
from enum import Enum, IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import FixedTypeList, UBInt8, UBInt16, UBInt32

# Third-party imports


__all__ = ('Ipv6ExtHdrFlags', 'Match', 'MatchField', 'MatchType',
           'OxmExperimenterHeader', 'OxmOfbMatchField', 'VlanId')


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


class MatchField(IntEnum):
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


class OxmOfbMatchField(IntEnum):
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


class OxmHeader(GenericStruct):
    """Generic Openflow EXtensible Match header.

    Abstract class that can be instanciated as Match or OxmExperimenterHeader.
    """

    pass


class Match(OxmHeader):
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
    oxm_field1 = UBInt8(enum_ref=OxmOfbMatchField)
    oxm_field2 = UBInt8(enum_ref=OxmOfbMatchField)
    oxm_field3 = UBInt8(enum_ref=OxmOfbMatchField)
    oxm_field4 = UBInt8(enum_ref=OxmOfbMatchField)

    def __init__(self, match_type=None, length=None, oxm_field1=None,
                 oxm_field2=None, oxm_field3=None, oxm_field4=None):
        """Describe the flow match header structure.

        Args:
            match_type (MatchType): One of OFPMT_* (MatchType) items.
            length (int): Length of Match (excluding padding) followed by
                          Exactly (length - 4) (possibly 0) bytes containing
                          OXM TLVs, then exactly ((length + 7)/8*8 - length)
                          (between 0 and 7) bytes of all-zero bytes.
            oxm_field1 (OXMClass): Sample description.
            oxm_field2 (OXMClass): Sample description.
            oxm_field3 (OXMClass): Sample description.
            oxm_field4 (OXMClass): Sample description.
        """
        super().__init__()
        self.match_type = match_type
        self.length = length
        self.oxm_field1 = oxm_field1
        self.oxm_field2 = oxm_field2
        self.oxm_field3 = oxm_field3
        self.oxm_field4 = oxm_field4


class OxmExperimenterHeader(OxmHeader):
    """Header for OXM experimenter match fields."""

    #: oxm_class = OFPXMC_EXPERIMENTER
    oxm_header = UBInt32(OxmOfbMatchField.OFPXMC_EXPERIMENTER,
                         enum_ref=OxmOfbMatchField)
    #: Experimenter ID which takes the same form as in struct
    #:     ofp_experimenter_header
    experimenter = UBInt32()

    def __init__(self, experimenter=None):
        """Header for OXM experimenter match fields.

        Args:
            - experimenter (int): Experimenter ID which takes the same form as
                in struct ofp_experimenter_header
        """
        super().__init__()
        self.experimenter = experimenter


class ListOfOxmHeader(FixedTypeList):
    """List of Openflow EXtensible Match header instances.

    Represented by instances of OxmHeader.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (OxmHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=OxmHeader, items=items)
