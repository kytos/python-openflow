"""Defines flow statistics structures and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from common import base
from common import basic_types

# Enums


class OFPMatchType (enum.Enum):
    """
    The "standard" type corresponds to ofp_match and must be supported by all
    OpenFlow switches. Extensions that define other match types may be
    published on the OpenFlow wiki. Support for extensions is optional.
    """
    OFPMT_STANDARD = 0      # Deprecated in OpenFlow >= 1.2
    OFPMT_OXM = 1           # OpenFlow Extensible Match (OF >= 1.2)


class OFPFlowWildCards (enum.Enum):
    """
    Wildcards used to identify flows.
    """
    OFPFW_IN_PORT = 1 << 0      # Switch input port
    OFPFW_DL_VLAN = 1 << 1      # VLAN id
    OFPFW_DL_VLAN_PCP = 1 << 2  # VLAN priority
    OFPFW_DL_TYPE = 1 << 3      # Ethernet Frame Type
    OFPFW_NW_TOS = 1 << 4       # IP ToS (DSCP field, 6 bits)
    OFPFW_NW_PROTO = 1 << 5     # IP Protocol
    OFPFW_TP_SRC = 1 << 6       # TCP/UDP/SCTP source port
    OFPFW_TP_DST = 1 << 7       # TCP/UDP/SCTP destination port
    OFPFW_MPLS_LABEL = 1 << 8   # MPLS label
    OFPFW_ALL = 1 << 9          # MPLS TC


class OFPVlanID (enum.Enum):
    OFPVID_ANY = 0xfffe
    OFPVID_NONE = 0xffff


# Classes (Structs)


class OFPMatch (base.GenericStruct):
    """
    Describes a flow entry. Fields to match against flows
    """

    # TODO: Need to define where constants will be set.
    # Attributes
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    in_port = basic_types.UBInt32()
    wildcards = basic_types.UBInt32()
    dl_src = basic_types.UBInt8Array(length=OFP_ETH_ALEN)
    dl_src_mask = basic_types.UBInt8Array(length=OFP_ETH_ALEN)
    dl_dst = basic_types.UBInt8Array(length=OFP_ETH_ALEN)
    dl_dst_mask = basic_types.UBInt8Array(length=OFP_ETH_ALEN)
    dl_vlan = basic_types.UBInt16()
    dl_vlan_pcp = basic_types.UBInt8()
    pad1 = basic_types.UBInt8Array(length=1)
    dl_type = basic_types.UBInt16()
    nw_tos = basic_types.UBInt8()
    nw_proto = basic_types.UBInt8()

    nw_src = basic_types.UBInt32()
    nw_src_mask = basic_types.UBInt32()
    nw_dst = basic_types.UBInt32()
    nw_dst_mask = basic_types.UBInt32()
    tp_src = basic_types.UBInt16()
    tp_dst = basic_types.UBInt16()
    mpls_label = basic_types.UBInt32()
    mpls_tc = basic_types.UBInt8()
    pad2 = basic_types.UBInt8Array(length=3)
    metadata = basic_types.UBInt64()
    metadata_mask = basic_types.UBInt64()
