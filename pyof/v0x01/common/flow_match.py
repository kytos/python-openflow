"""Defines flow statistics structures and related items."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

__all__ = ['Match', 'FlowWildCards']


class FlowWildCards(base.GenericBitMask):
    """Wildcards used to identify flows.

    ``OFPFW_NW_SRC_*``: IP source address wildcard bit count. 0 is exact match,
    1 ignores the LSB, 2 ignores the 2 least-significant bits, ..., 32 and
    higher wildcard the entire field.  This is the *opposite* of the usual
    convention where e.g. /24 indicates that 8 bits (not 24 bits) are
    wildcarded.

    ``OFPFW_NW_DST_*``: IP destination address wildcard bit count. Same format
    as source.
    """

    #: Switch input port.
    OFPFW_IN_PORT = 1 << 0
    #: VLAN id.
    OFPFW_DL_VLAN = 1 << 1
    #: Ethernet source address.
    OFPFW_DL_SRC = 1 << 2
    #: Ethernet destination address.
    OFPFW_DL_DST = 1 << 3
    #: Ethernet frame type.
    OFPFW_DL_TYPE = 1 << 4
    #: IP protocol.
    OFPFW_NW_PROTO = 1 << 5
    #: TCP/UDP source port.
    OFPFW_TP_SRC = 1 << 6
    #: TCP/UDP destination port.
    OFPFW_TP_DST = 1 << 7

    # See class docstring
    OFPFW_NW_SRC_SHIFT = 8
    OFPFW_NW_SRC_BITS = 6
    OFPFW_NW_SRC_MASK = ((1 << OFPFW_NW_SRC_BITS) - 1) << OFPFW_NW_SRC_SHIFT
    OFPFW_NW_SRC_ALL = 32 << OFPFW_NW_SRC_SHIFT

    # See class docstring
    OFPFW_NW_DST_SHIFT = 14
    OFPFW_NW_DST_BITS = 6
    OFPFW_NW_DST_MASK = ((1 << OFPFW_NW_DST_BITS) - 1) << OFPFW_NW_DST_SHIFT
    OFPFW_NW_DST_ALL = 32 << OFPFW_NW_DST_SHIFT
    OFPFW_DL_VLAN_PCP = 1 << 20
    OFPFW_NW_TOS = 1 << 21

    #: Wildcard all fields.
    OFPFW_ALL = ((1 << 22) - 1)


# Classes


class Match(base.GenericStruct):
    """Describes a flow entry. Fields to match against flows."""

    wildcards = basic_types.UBInt32(enum_ref=FlowWildCards)
    in_port = basic_types.UBInt16()
    dl_src = basic_types.HWAddress()
    dl_dst = basic_types.HWAddress()
    dl_vlan = basic_types.UBInt16()
    dl_vlan_pcp = basic_types.UBInt8()
    #: Align to 64-bits.
    pad1 = basic_types.PAD(1)
    dl_type = basic_types.UBInt16()
    nw_tos = basic_types.UBInt8()
    nw_proto = basic_types.UBInt8()
    #: Align to 64-bits.
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
        #: Wildcard fields.
        self.wildcards = wildcards
        #: Input switch port.
        self.in_port = in_port
        #: Ethernet source address.
        self.dl_src = dl_src
        #: Ethernet destination address.
        self.dl_dst = dl_dst
        #: Input VLAN id.
        self.dl_vlan = dl_vlan
        #: Input VLAN priority.
        self.dl_vlan_pcp = dl_vlan_pcp
        #: Ethernet frame type.
        self.dl_type = dl_type
        #: IP ToS (actually DSCP field, 6 bits).
        self.nw_tos = nw_tos
        #: IP protocol or lower 8 bits of ARP opcode.
        self.nw_proto = nw_proto
        #: IP source address.
        self.nw_src = nw_src
        #: IP destination address.
        self.nw_dst = nw_dst
        #: TCP/UDP source port.
        self.tp_src = tp_src
        #: TCP/UDP destination port.
        self.tp_dst = tp_dst
