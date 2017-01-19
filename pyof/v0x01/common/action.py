"""Defines actions that may be associated with flows packets."""

# System imports

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericStruct
from pyof.foundation.basic_types import (HWAddress, Pad, UBInt8, UBInt16,
                                         UBInt32)

# Third-party imports

__all__ = ('ActionType', 'ActionHeader', 'ActionOutput', 'ActionEnqueue',
           'ActionVlanVid', 'ActionVlanPCP', 'ActionDLAddr', 'ActionNWAddr',
           'ActionNWTos', 'ActionTPPort', 'ActionVendorHeader')

# Enums


class ActionType(GenericBitMask):
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


class ActionHeader(GenericStruct):
    """Defines the Header that is common to all actions."""

    action_type = UBInt16(enum_ref=ActionType)
    length = UBInt16()
    #: Pad for 64-bit alignment.
    pad = Pad(4)

    _allowed_types = ()

    def __init__(self, action_type=None, length=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): The type of the action.
            length (int): Length of action, including this header.
        """
        super().__init__()
        self.action_type = action_type
        self.length = length

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            Exception: If there is a struct unpacking error.
        """
        self.action_type = UBInt16(enum_ref=ActionType)
        self.action_type.unpack(buff, offset)

        for cls in ActionHeader.__subclasses__():
            if self.action_type.value in cls.get_allowed_types():
                self.__class__ = cls
                break

        super().unpack(buff, offset)

    @classmethod
    def get_allowed_types(cls):
        """Return allowed types for the class."""
        return cls._allowed_types


class ActionOutput(ActionHeader):
    """Defines the actions output.

    Action structure for :attr:`ActionType.OFPAT_OUTPUT`, which sends packets
    out :attr:`port`. When the :attr:`port` is the
    :attr:`.Port.OFPP_CONTROLLER`, :attr:`max_length` indicates the max number
    of bytes to send. A :attr:`max_length` of zero means no bytes of the packet
    should be sent.
    """

    action_type = UBInt16(ActionType.OFPAT_OUTPUT, enum_ref=ActionType)
    length = UBInt16(8)
    port = UBInt16()
    max_length = UBInt16()

    _allowed_types = ActionType.OFPAT_OUTPUT,
    _removed_attributes = ['pad']

    def __init__(self, port=None, max_length=0):
        """The following constructor parameters are optional.

        Args:
            port (:class:`Port` or :class:`int`): Output port.
            max_length (int): Max length to send to controller.
        """
        super().__init__()
        self.port = port
        self.max_length = max_length


class ActionEnqueue(ActionHeader):
    """Send packets to a queue's port.

    A switch may support only queues that are tied to specific PCP/TOS bits.
    In that case, we cannot map an arbitrary flow to a specific queue,
    therefore the action ENQUEUE is not supported. The user can still use
    these queues and map flows to them by setting the relevant fields
    (TOS, VLAN PCP).
    """

    action_type = UBInt16(ActionType.OFPAT_ENQUEUE, enum_ref=ActionType)
    length = UBInt16(16)
    port = UBInt16()
    #: Pad for 64-bit alignment.
    pad = Pad(6)
    queue_id = UBInt32()

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = ActionType.OFPAT_ENQUEUE,

    def __init__(self, port=None, queue_id=None):
        """The following constructor parameters are optional.

        Args:
            port (physical port or :attr:`.Port.OFPP_IN_PORT`): Queue's port.
            queue_id (int): Where to enqueue the packets.
        """
        super().__init__()
        self.port = port
        self.queue_id = queue_id


class ActionVlanVid(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_VLAN_VID`.

    .. note:: The vlan_vid field is 16 bits long,
              when an actual VLAN id is only 12 bits.
              The value 0xffff is used to indicate that no VLAN id was set
    """

    action_type = UBInt16(ActionType.OFPAT_SET_VLAN_VID, enum_ref=ActionType)
    length = UBInt16(8)
    vlan_id = UBInt16()
    #: Pad for bit alignment.
    pad2 = Pad(2)

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = ActionType.OFPAT_SET_VLAN_VID,

    def __init__(self, vlan_id=None):
        """The following constructor parameters are optional.

        Args:
            vlan_id (int): VLAN priority.
        """
        super().__init__()
        self.vlan_id = vlan_id


class ActionVlanPCP(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_VLAN_PCP`."""

    action_type = UBInt16(ActionType.OFPAT_SET_VLAN_PCP, enum_ref=ActionType)
    length = UBInt16(8)
    vlan_pcp = UBInt8()
    #: Pad for bit alignment.
    pad = Pad(3)

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = ActionType.OFPAT_SET_VLAN_PCP,

    def __init__(self, vlan_pcp=None):
        """The following constructor parameters are optional.

        Args:
            vlan_pcp (int): VLAN Priority.

        .. note:: The vlan_pcp field is 8 bits long,
                  but only the lower 3 bits have meaning.
        """
        super().__init__()
        self.vlan_pcp = vlan_pcp


class ActionDLAddr(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_DL_SRC` or _DST."""

    action_type = UBInt16(enum_ref=ActionType)
    length = UBInt16(16)
    dl_addr = HWAddress()
    #: Pad for bit alignment.
    pad = Pad(6)

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = (ActionType.OFPAT_SET_DL_SRC, ActionType.OFPAT_SET_DL_DST)

    def __init__(self, action_type=None, dl_addr=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): :attr:`~ActionType.OFPAT_SET_DL_SRC` or
                :attr:`~ActionType.OFPAT_SET_DL_DST`.
            dl_addr (:class:`~.HWAddress`): Ethernet address.
                Defaults to None.
        """
        super().__init__()
        self.action_type = action_type
        self.dl_addr = dl_addr


class ActionNWAddr(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_NW_SRC` or _DST."""

    action_type = UBInt16(enum_ref=ActionType)
    length = UBInt16(8)
    nw_addr = UBInt32()

    _removed_attributes = ['pad']
    _allowed_types = (ActionType.OFPAT_SET_NW_SRC, ActionType.OFPAT_SET_NW_DST)

    def __init__(self, action_type=None, nw_addr=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): :attr:`~ActionType.OFPAT_SET_NW_SRC` or
                :attr:`~ActionType.OFPAT_SET_NW_DST`.
            nw_addr (int): IP Address.
        """
        super().__init__()
        self.action_type = action_type
        self.nw_addr = nw_addr


class ActionNWTos(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_NW_TOS`.

    .. note:: The nw_tos field is the 6 upper bits of the ToS field to set,
              in the original bit positions (shifted to the left by 2).
    """

    action_type = UBInt16(enum_ref=ActionType)
    length = UBInt16(8)
    nw_tos = UBInt8()
    #: Pad for bit alignment.
    pad = Pad(3)

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = ActionType.OFPAT_SET_NW_TOS,

    def __init__(self, action_type=None, nw_tos=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): :attr:`~ActionType.OFPAT_SET_NW_SRC` or
                :attr:`~ActionType.OFPAT_SET_NW_DST`.
            nw_tos (int): IP ToS (DSCP field, 6 bits).
        """
        super().__init__()
        self.action_type = action_type
        self.nw_tos = nw_tos


class ActionTPPort(ActionHeader):
    """Action structure for :attr:`ActionType.OFPAT_SET_TP_SRC` or _DST."""

    action_type = UBInt16(enum_ref=ActionType)
    length = UBInt16(8)
    tp_port = UBInt16()
    #: Pad for bit alignment.
    pad = Pad(2)

    #: The parent class `pad` attribute need to be repositioned.
    _removed_attributes = ['pad']
    _allowed_types = (ActionType.OFPAT_SET_TP_SRC, ActionType.OFPAT_SET_TP_DST)

    def __init__(self, action_type=None, tp_port=None):
        """The following constructor parameters are optional.

        Args:
            action_type (ActionType): :attr:`~ActionType.OFPAT_SET_TP_SRC` or
                :attr:`~ActionType.OFPAT_SET_TP_DST`.
            tp_port (int): TCP/UDP/other port to set.
        """
        super().__init__()
        self.action_type = action_type
        self.tp_port = tp_port


class ActionVendorHeader(ActionHeader):
    """Action header for :attr:`ActionType.OFPAT_VENDOR`.

    The rest of the body is vendor-defined.
    """

    action_type = UBInt16(ActionType.OFPAT_VENDOR, enum_ref=ActionType)
    length = UBInt16()
    vendor = UBInt32()

    _removed_attributes = ['pad']
    _allowed_types = ActionType.OFPAT_VENDOR,

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
