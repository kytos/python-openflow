"""Defines actions that may be associated with flows packets."""

# System imports
import enum

# Local source tree imports
from pyof.v0x01.foundation import base, basic_types


# Third-party imports


__all__ = ('ActionType', 'ActionHeader', 'ActionOutput', 'ActionEnqueue',
           'ActionVlanVid', 'ActionVlanPCP', 'ActionDLAddr', 'ActionNWAddr',
           'ActionNWTos', 'ActionTPPort', 'ActionVendorHeader')

# Enums


class ActionType(enum.Enum):
    """Actions associated with flows and packets."""

    #: Output to switch port.
    OFPAT_OUTPUT = 0
    #: Set the 802.1q VLAN id.
    OFPAT_SET_VLAN_VID = 1
    #: Set the 802.1q priority.
    OFPAT_SET_VLAN_PCP = 2
    #: Strip the 802.1q header.
    OFPAT_STRIP_VLAN = 3
    #: Ethernet source address.
    OFPAT_SET_DL_SRC = 4
    #: Ethernet destination address.
    OFPAT_SET_DL_DST = 5
    #: IP source address.
    OFPAT_SET_NW_SRC = 6
    #: IP destination address.
    OFPAT_SET_NW_DST = 7
    #: IP ToS (DSCP field, 6 bits).
    OFPAT_SET_NW_TOS = 8
    #: TCP/UDP source port.
    OFPAT_SET_TP_SRC = 9
    #: TCP/UDP destination port.
    OFPAT_SET_TP_DST = 10
    #: Output to queue.
    OFPAT_ENQUEUE = 11
    #: Vendor specific.
    OFPAT_VENDOR = 0xffff


# Classes


class ActionHeader(base.GenericStruct):
    """Defines the Header that is common to all actions."""

    action_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16()
    #: Pad for 64-bit alignment.
    pad = basic_types.PAD(4)

    def __init__(self, action_type=None, length=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): The type of the action.
            length (int): Length of action, including this header.
        """
        super().__init__()
        self.action_type = action_type
        self.length = length


class ActionOutput(base.GenericStruct):
    """Defines the actions output.

    Action structure for :attr:`ActionType.OFPAT_OUTPUT`, which sends packets
    out :attr:`port`. When the :attr:`port` is the
    :attr:`.Port.OFPP_CONTROLLER`, :attr:`max_length` indicates the max number
    of bytes to send. A :attr:`max_length` of zero means no bytes of the packet
    should be sent.
    """

    type = basic_types.UBInt16(ActionType.OFPAT_OUTPUT,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    port = basic_types.UBInt16()
    max_length = basic_types.UBInt16()

    def __init__(self, port=None, max_length=None):
        """The following constructor parameters are optional.

        Args:
            port (:class:`Port` or :class:`int`): Output port.
            max_length (int): Max length to send to controller.
        """
        super().__init__()
        self.port = port
        self.max_length = max_length


class ActionEnqueue(base.GenericStruct):
    """Send packets to a queue's port.

    A switch may support only queues that are tied to specific PCP/TOS bits.
    In that case, we cannot map an arbitrary flow to a specific queue,
    therefore the action ENQUEUE is not supported. The user can still use
    these queues and map flows to them by setting the relevant fields
    (TOS, VLAN PCP).
    """

    type = basic_types.UBInt16(ActionType.OFPAT_ENQUEUE,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(16)
    port = basic_types.UBInt16()
    #: Pad for 64-bit alignment.
    pad = basic_types.PAD(6)
    queue_id = basic_types.UBInt32()

    def __init__(self, port=None, queue_id=None):
        """The following constructor parameters are optional.

        Args:
            port (physical port or :attr:`.Port.OFPP_IN_PORT`): Queue's port.
            queue_id (int): Where to enqueue the packets.
        """
        super().__init__()
        self.port = port
        self.queue_id = queue_id


class ActionVlanVid(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_VLAN_VID`.

    .. note:: The vlan_vid field is 16 bits long,
              when an actual VLAN id is only 12 bits.
              The value 0xffff is used to indicate that no VLAN id was set
    """

    type = basic_types.UBInt16(ActionType.OFPAT_SET_VLAN_PCP,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    vlan_id = basic_types.UBInt16()
    #: Pad for bit alignment.
    pad2 = basic_types.PAD(2)

    def __init__(self, vlan_id=None):
        """The following constructor parameters are optional.

        Args:
            vlan_id (int): VLAN priority.
        """
        super().__init__()
        self.vlan_id = vlan_id


class ActionVlanPCP(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_VLAN_PCP`."""

    type = basic_types.UBInt16(ActionType.OFPAT_SET_VLAN_PCP,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    vlan_pcp = basic_types.UBInt8()
    #: Pad for bit alignment.
    pad = basic_types.PAD(3)

    def __init__(self, vlan_pcp=None):
        """The following constructor parameters are optional.

        Args:
            vlan_pcp (int): VLAN Priority.

        .. note:: The vlan_pcp field is 8 bits long,
                  but only the lower 3 bits have meaning.
        """
        super().__init__()
        self.vlan_pcp = vlan_pcp


class ActionDLAddr(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_DL_SRC` or _DST."""

    dl_addr_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(16)
    dl_addr = basic_types.HWAddress()
    #: Pad for bit alignment.
    pad = basic_types.PAD(6)

    def __init__(self, dl_addr_type=None, dl_addr=None):
        """The following constructor parameters are optional.

        Args:
            dl_addr_type (ActionType): :attr:`~ActionType.OFPAT_SET_DL_SRC` or
                :attr:`~ActionType.OFPAT_SET_DL_DST`.
            dl_addr (:class:`~.basic_types.HWAddress`): Ethernet address.
                Defaults to None.
        """
        super().__init__()
        self.dl_addr_type = dl_addr_type
        self.dl_addr = dl_addr


class ActionNWAddr(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_NW_SRC` or _DST."""

    nw_addr_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    nw_addr = basic_types.UBInt32()

    def __init__(self, nw_addr_type=None, nw_addr=None):
        """The following constructor parameters are optional.

        Args:
            nw_addr_type (ActionType): :attr:`~ActionType.OFPAT_SET_NW_SRC` or
                :attr:`~ActionType.OFPAT_SET_NW_DST`.
            nw_addr (int): IP Address.
        """
        super().__init__()
        self.nw_addr_type = nw_addr_type
        self.nw_addr = nw_addr


class ActionNWTos(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_NW_TOS`.

    .. note:: The nw_tos field is the 6 upper bits of the ToS field to set,
              in the original bit positions (shifted to the left by 2).
    """

    nw_tos_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    nw_tos = basic_types.UBInt8()
    #: Pad for bit alignment.
    pad = basic_types.PAD(3)

    def __init__(self, nw_tos_type=None, nw_tos=None):
        """The following constructor parameters are optional.

        Args:
            nw_tos_type (ActionType): :attr:`~ActionType.OFPAT_SET_NW_SRC` or
                :attr:`~ActionType.OFPAT_SET_NW_SRC`.
            nw_tos (int): IP ToS (DSCP field, 6 bits).
        """
        super().__init__()
        self.nw_tos_type = nw_tos_type
        self.nw_tos = nw_tos


class ActionTPPort(base.GenericStruct):
    """Action structure for :attr:`ActionType.OFPAT_SET_TP_SRC` or _DST."""

    tp_port_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    tp_port = basic_types.UBInt16()
    #: Pad for bit alignment.
    pad = basic_types.PAD(2)

    def __init__(self, tp_port_type=None, tp_port=None):
        """The following constructor parameters are optional.

        Args:
            tp_port_type (ActionType): :attr:`~ActionType.OFPAT_SET_TP_SRC` or
                :attr:`~ActionType.OFPAT_SET_TP_DST`.
            tp_port (int): TCP/UDP/other port to set.
        """
        super().__init__()
        self.tp_port_type = tp_port_type
        self.tp_port = tp_port


class ActionVendorHeader(base.GenericStruct):
    """Action header for :attr:`ActionType.OFPAT_VENDOR`.

    The rest of the body is vendor-defined.
    """

    type = basic_types.UBInt16(ActionType.OFPAT_VENDOR,
                               enum_ref=ActionType)
    length = basic_types.UBInt16()
    vendor = basic_types.UBInt32()

    def __init__(self, length=None, vendor=None):
        """The following constructor parameters are optional.

        Args:
            length (int): Length is a multiple of 8.
            vender (int): Vendor ID with the same form as in VendorHeader.
                Defaults to None.
        """
        super().__init__()
        self.length = length
        self.vendor = vendor
