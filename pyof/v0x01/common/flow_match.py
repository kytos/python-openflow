"""Defines flow statistics structures and related items."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation.base import (GenericBitMask, GenericMessage,
                                        GenericStruct)
from pyof.v0x01.foundation.basic_types import (PAD, HWAddress, UBInt8, UBInt16,
                                               UBInt32)

__all__ = ('Match', 'FlowWildCards')


class FlowWildCards(GenericBitMask):
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


class Match(GenericStruct):
    """Describes a flow entry. Fields to match against flows."""

    wildcards = UBInt32(enum_ref=FlowWildCards)
    in_port = UBInt16()
    dl_src = HWAddress()
    dl_dst = HWAddress()
    dl_vlan = UBInt16()
    dl_vlan_pcp = UBInt8()
    #: Align to 64-bits.
    pad1 = PAD(1)
    dl_type = UBInt16()
    nw_tos = UBInt8()
    nw_proto = UBInt8()
    #: Align to 64-bits.
    pad2 = PAD(2)
    nw_src = UBInt32()
    nw_dst = UBInt32()
    tp_src = UBInt16()
    tp_dst = UBInt16()

    def __init__(self, wildcards=None, in_port=None, dl_src=None, dl_dst=None,
                 dl_vlan=None, dl_vlan_pcp=None, dl_type=None,
                 nw_tos=None, nw_proto=None, nw_src=None,
                 nw_dst=None, tp_src=None, tp_dst=None):
        """All the constructor parameters below are optional.

        Args:
            wildcards (FlowWildCards): Wildcards fields.
            in_port (int): Input switch port.
            dl_src (HWAddress): Ethernet source address.
            dl_dst (HWAddress): Ethernet destination address.
            dl_vlan (int): Input VLAN id.
            dl_vlan_pcp (int): Input VLAN priority.
            dl_type (int): Ethernet frame type.
            nw_tos (int): IP ToS (actually DSCP field, 6 bits).
            nw_proto (int): IP protocol or lower 8 bits of ARP opcode.
            nw_src (int): IP source address.
            nw_dst (int): IP destination address.
            tp_src (int): TCP/UDP source port.
            tp_dst (int): TCP/UDP destination port.
        """
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
