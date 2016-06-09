"""Defines flow statistics structures and related items"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class FlowWildCards(base.GenericBitMask):
    """
    Wildcards used to identify flows.

        OFPFW_IN_PORT   # Switch input port.
        OFPFW_DL_VLAN   # VLAN id.
        OFPFW_DL_SRC    # Ethernet source address.
        OFPFW_DL_DST    # Ethernet destination address.
        OFPFW_DL_TYPE   # Ethernet frame type.
        OFPFW_NW_PROTO  # IP protocol.
        OFPFW_TP_SRC    # TCP/UDP source port.
        OFPFW_TP_DST    # TCP/UDP destination port.

    """

    OFPFW_IN_PORT = 1 << 0
    OFPFW_DL_VLAN = 1 << 1
    OFPFW_DL_SRC = 1 << 2
    OFPFW_DL_DST = 1 << 3
    OFPFW_DL_TYPE = 1 << 4
    OFPFW_NW_PROTO = 1 << 5
    OFPFW_TP_SRC = 1 << 6
    OFPFW_TP_DST = 1 << 7

    # IP source address wildcard bit count. 0 is exact match, 1 ignores the
    # LSB, 2 ignores the 2 least-significant bits, ..., 32 and higher wildcard
    # the entire field.  This is the *opposite* of the usual convention where
    # e.g. /24 indicates that 8 bits (not 24 bits) are wildcarded.

    OFPFW_NW_SRC_SHIFT = 8
    OFPFW_NW_SRC_BITS = 6
    OFPFW_NW_SRC_MASK = ((1 << OFPFW_NW_SRC_BITS) - 1) << OFPFW_NW_SRC_SHIFT
    OFPFW_NW_SRC_ALL = 32 << OFPFW_NW_SRC_SHIFT

    # IP destination address wildcard bit count. Same format as source.
    OFPFW_NW_DST_SHIFT = 14
    OFPFW_NW_DST_BITS = 6
    OFPFW_NW_DST_MASK = ((1 << OFPFW_NW_DST_BITS) - 1) << OFPFW_NW_DST_SHIFT
    OFPFW_NW_DST_ALL = 32 << OFPFW_NW_DST_SHIFT
    OFPFW_DL_VLAN_PCP = 1 << 20
    OFPFW_NW_TOS = 1 << 21

    # Wildcard all fields.
    OFPFW_ALL = ((1 << 22) - 1)


# Classes


class Match(base.GenericStruct):
    """Describes a flow entry. Fields to match against flows

    :param wildcards:            Wildcard fields.
    :param in_port:              Input switch port.
    :param dl_src[OFP_ETH_ALEN]: Ethernet source address.
    :param dl_dst[OFP_ETH_ALEN]: Ethernet destination address.
    :param dl_vlan:              Input VLAN id.
    :param dl_vlan_pcp:          Input VLAN priority.
    :param pad1[1]:              Align to 64-bits.
    :param dl_type:              Ethernet frame type.
    :param nw_tos:               IP ToS (actually DSCP field, 6 bits).
    :param nw_proto:             IP protocol or lower 8 bits of ARP opcode
    :param pad2[2]:              Align to 64-bits.
    :param nw_src:               IP source address.
    :param nw_dst:               IP destination address.
    :param tp_src:               TCP/UDP source port.
    :param tp_dst:               TCP/UDP destination port.
    """
    # Attributes
    wildcards = basic_types.UBInt32(enum_ref=FlowWildCards)
    in_port = basic_types.UBInt16()
    dl_src = basic_types.HWAddress()
    dl_dst = basic_types.HWAddress()
    dl_vlan = basic_types.UBInt16()
    dl_vlan_pcp = basic_types.UBInt8()
    pad1 = basic_types.PAD(1)
    dl_type = basic_types.UBInt16()
    nw_tos = basic_types.UBInt8()
    nw_proto = basic_types.UBInt8()
    pad2 = basic_types.PAD(2)
    nw_src = basic_types.UBInt32()
    nw_dst = basic_types.UBInt32()
    tp_src = basic_types.UBInt16()
    tp_dst = basic_types.UBInt16()

    def __init__(self, wildcards=None, in_port=None, dl_src=None, dl_dst=None,
                 dl_vlan=None, dl_vlan_pcp=None, dl_type=None,
                 nw_tos=None, nw_proto=None, nw_src=None,
                 nw_dst=None, tp_src=None, tp_dst=None):
        super().__init__()
        self.wildcards = wildcards
        self.in_port = in_port
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.dl_vlan = dl_vlan
        self.dl_vlan_pcp = dl_vlan_pcp
        self.dl_type = dl_type
        self.nw_tos = nw_tos
        self.nw_proto = nw_proto
        self.nw_src = nw_src
        self.nw_dst = nw_dst
        self.tp_src = tp_src
        self.tp_dst = tp_dst
