"""Defines flow statistics structures and related items."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericStruct
from pyof.foundation.basic_types import (
    HWAddress, IPAddress, Pad, UBInt8, UBInt16, UBInt32)

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
    wildcards = UBInt32(value=FlowWildCards.OFPFW_ALL, enum_ref=FlowWildCards)
    #: Input switch port.
    in_port = UBInt16(0)
    #: Ethernet source address. (default: '00:00:00:00:00:00')
    dl_src = HWAddress()
    #: Ethernet destination address. (default: '00:00:00:00:00:00')
    dl_dst = HWAddress()
    #: Input VLAN id. (default: 0)
    dl_vlan = UBInt16(0)
    #: Input VLAN priority. (default: 0)
    dl_vlan_pcp = UBInt8(0)
    #: Align to 64-bits.
    pad1 = Pad(1)
    #: Ethernet frame type. (default: 0)
    dl_type = UBInt16(0)
    #: IP ToS (actually DSCP field, 6 bits). (default: 0)
    nw_tos = UBInt8(0)
    #: IP protocol or lower 8 bits of ARP opcode. (default: 0)
    nw_proto = UBInt8(0)
    #: Align to 64-bits.
    pad2 = Pad(2)
    #: IP source address. (default: '0.0.0.0/32')
    nw_src = IPAddress()
    #: IP destination address. (default: '0.0.0.0/32')
    nw_dst = IPAddress()
    #: TCP/UDP source port. (default: 0)
    tp_src = UBInt16(0)
    #: TCP/UDP destination port. (default: 0)
    tp_dst = UBInt16(0)

    def __init__(self, **kwargs):
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
            nw_src (IPAddress): IP source address. (default: '0.0.0.0/32')
            nw_dst (IPAddress): IP destination address. (default: '0.0.0.0/32')
            tp_src (int): TCP/UDP source port. (default: 0)
            tp_dst (int): TCP/UDP destination port. (default: 0)
        """
        super().__init__()
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __setattr__(self, name, value):

        # converts string ip_address to IPAddress
        if isinstance(getattr(Match, name), IPAddress) and \
                not isinstance(value, IPAddress):
            if isinstance(value, list):
                value = ".".join(str(x) for x in value)
            value = IPAddress(value)  # noqa
        # convertstring or list of hwaddress to HWAddress
        elif isinstance(getattr(Match, name), HWAddress) and \
                not isinstance(value, HWAddress):
            if isinstance(value, list):
                values = ["{0:0{1}x}".format(x, 2) for x in value]
                value = ":".join(values)
            value = HWAddress(value)

        super().__setattr__(name, value)
        self.fill_wildcards(name, value)

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        Do nothing, since the _length is already defined and it is just a Pad.
        Keep buff and offset just for compability with other unpack methods.

        Args:
            buff: Buffer where data is located.
            offset (int): Where data stream begins.
        """
        super().unpack(buff, offset)
        self.wildcards = UBInt32(value=FlowWildCards.OFPFW_ALL,
                                 enum_ref=FlowWildCards)
        self.wildcards.unpack(buff, offset)

    def fill_wildcards(self, field=None, value=0):
        """Update wildcards attribute.

        This method update a wildcards considering the attributes of the
        current instance.

        Args:
            field (str): Name of the updated field.
            value (GenericType): New value used in the field.
        """
        if field in [None, 'wildcards'] or isinstance(value, Pad):
            return

        default_value = getattr(Match, field)
        if isinstance(default_value, IPAddress):
            if field == 'nw_dst':
                self.wildcards |= FlowWildCards.OFPFW_NW_DST_MASK
                shift = FlowWildCards.OFPFW_NW_DST_SHIFT
            else:
                self.wildcards |= FlowWildCards.OFPFW_NW_SRC_MASK
                shift = FlowWildCards.OFPFW_NW_SRC_SHIFT
            wildcard = (value.max_prefix - value.netmask) << shift
            self.wildcards -= wildcard
        else:
            wildcard_field = "OFPFW_{}".format(field.upper())
            wildcard = getattr(FlowWildCards, wildcard_field)

            if value == default_value and not (self.wildcards & wildcard) or \
               value != default_value and (self.wildcards & wildcard):
                self.wildcards ^= wildcard
