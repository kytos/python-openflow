"""Defines flow statistics structures and related items."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericStruct
from pyof.foundation.basic_types import (HWAddress, Pad, UBInt8, UBInt16,
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

    #: Wildcards fields.
    wildcards = UBInt32(enum_ref=FlowWildCards)
    #: Input switch port.
    in_port = UBInt16()
    #: Ethernet source address. (default: '00:00:00:00:00:00')
    dl_src = HWAddress()
    #: Ethernet destination address. (default: '00:00:00:00:00:00')
    dl_dst = HWAddress()
    #: Input VLAN id. (default: 0)
    dl_vlan = UBInt16()
    #: Input VLAN priority. (default: 0)
    dl_vlan_pcp = UBInt8()
    #: Align to 64-bits.
    pad1 = Pad(1)
    #: Ethernet frame type. (default: 0)
    dl_type = UBInt16()
    #: IP ToS (actually DSCP field, 6 bits). (default: 0)
    nw_tos = UBInt8()
    #: IP protocol or lower 8 bits of ARP opcode. (default: 0)
    nw_proto = UBInt8()
    #: Align to 64-bits.
    pad2 = Pad(2)
    #: IP source address. (default: 0)
    nw_src = UBInt32()
    #: IP destination address. (default: 0)
    nw_dst = UBInt32()
    #: TCP/UDP source port. (default: 0)
    tp_src = UBInt16()
    #: TCP/UDP destination port. (default: 0)
    tp_dst = UBInt16()

    def __init__(self, wildcards=FlowWildCards.OFPFW_ALL, in_port=0,
                 dl_src='00:00:00:00:00:00', dl_dst='00:00:00:00:00:00',
                 dl_vlan=0, dl_vlan_pcp=0, dl_type=0, nw_tos=0, nw_proto=0,
                 nw_src=0, nw_dst=0, tp_src=0, tp_dst=0):
        """All the constructor parameters below are optional.

        Args:
            wildcards (FlowWildCards): Wildcards fields. (Default: OFPFW_ALL)
            in_port (int): Input switch port. (default: 0)
            dl_src (HWAddress): Ethernet source address.
                (default: '00:00:00:00:00:00')
            dl_dst (HWAddress): Ethernet destination address.
                (default: '00:00:00:00:00:00')
            dl_vlan (int): Input VLAN id. (default: 0)
            dl_vlan_pcp (int): Input VLAN priority. (default: 0)
            dl_type (int): Ethernet frame type. (default: 0)
            nw_tos (int): IP ToS (actually DSCP field, 6 bits). (default: 0)
            nw_proto (int): IP protocol or lower 8 bits of ARP opcode.
                (default: 0)
            nw_src (int): IP source address. (default: 0)
            nw_dst (int): IP destination address. (default: 0)
            tp_src (int): TCP/UDP source port. (default: 0)
            tp_dst (int): TCP/UDP destination port. (default: 0)
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
