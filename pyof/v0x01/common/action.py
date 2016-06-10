"""Defines actions that may be associated with flows packets."""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Enums


class ActionType(enum.Enum):
    """Actions associated with flows and packets.

    Enums:
        OFPAT_OUTPUT        # Output to switch port.
        OFPAT_SET_VLAN_VID  # Set the 802.1q VLAN id.
        OFPAT_SET_VLAN_PCP  # Set the 802.1q priority.
        OFPAT_STRIP_VLAN    # Strip the 802.1q header.
        OFPAT_SET_DL_SRC    # Ethernet source address.
        OFPAT_SET_DL_DST    # Ethernet destination address.
        OFPAT_SET_NW_SRC    # IP source address.
        OFPAT_SET_NW_DST    # IP destination address.
        OFPAT_SET_NW_TOS    # IP ToS (DSCP field, 6 bits).
        OFPAT_SET_TP_SRC    # TCP/UDP source port.
        OFPAT_SET_TP_DST    # TCP/UDP destination port.
        OFPAT_ENQUEUE       # Output to queue.
    """
    OFPAT_OUTPUT = 0
    OFPAT_SET_VLAN_VID = 1
    OFPAT_SET_VLAN_PCP = 2
    OFPAT_STRIP_VLAN = 3
    OFPAT_SET_DL_SRC = 4
    OFPAT_SET_DL_DST = 5
    OFPAT_SET_NW_SRC = 6
    OFPAT_SET_NW_DST = 7
    OFPAT_SET_NW_TOS = 8
    OFPAT_SET_TP_SRC = 9
    OFPAT_SET_TP_DST = 10
    OFPAT_ENQUEUE = 11
    OFPAT_VENDOR = 0xffff


# Classes


class ActionHeader(base.GenericStruct):
    """Defines the Header that is common to all actions.

    :param action_type: One of OFPAT\_.
    :param length:     Length of action, including this header.
    :param pad:        Pad for 64-bit alignment.
    """
    action_type = basic_types.UBInt16(enum_ref=ActionType)
    # TODO: Implement is_valid specific method here to check length for
    #       'This is the length of action, including
    #        any padding to make it 64-bit aligned.'
    length = basic_types.UBInt16()
    pad = basic_types.PAD(4)

    def __init__(self, action_type=None, length=None):
        super().__init__()
        self.action_type = action_type
        self.length = length


class ActionOutput(base.GenericStruct):
    """Defines the actions output.

    Action structure for OFPAT_OUTPUT, which sends packets out ’port’.
    When the ’port’ is the OFPP_CONTROLLER, ’max_len’ indicates the max
    number of bytes to send. A ’max_len’ of zero means no bytes of the
    packet should be sent.
    # TODO : Implement validations considering the description above.

    :param type:       OFPAT_OUTPUT.
    :param length:     Length is 8.
    :param port:       Output port.
    :param max_length: Max length to send to controller.
    """
    type = basic_types.UBInt16(ActionType.OFPAT_OUTPUT,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    port = basic_types.UBInt16()
    max_length = basic_types.UBInt16()

    def __init__(self, port=None, max_length=None):
        super().__init__()
        self.port = port
        self.max_length = max_length


class ActionEnqueue(base.GenericStruct):
    """Send packets to given queue on port.

    A switch may support only queues that are tied to specific PCP/TOS bits.
    In that case, we cannot map an arbitrary flow to a specific queue,
    therefore the action ENQUEUE is not supported. The user can still use
    these queues and map flows to them by setting the relevant fields
    (TOS, VLAN PCP).

    :param type:       OFPAT_ENQUEUE.
    :param length:     Len is 16
    :param port:       Port that queue belongs. Should refer to a valid
                       physical port. (i.e. < OFPP_MAX) or OFPP_IN_PORT
                       # TODO : Validation
    :param pad:        Pad for 64-bit alignment.
    :param queue_id:   Where to enqueue the packets.
    """
    type = basic_types.UBInt16(ActionType.OFPAT_ENQUEUE,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(16)
    port = basic_types.UBInt16()
    pad = basic_types.PAD(6)
    queue_id = basic_types.UBInt32()

    def __init__(self, port=None, queue_id=None):
        super().__init__()
        self.port = port
        self.queue_id = queue_id


class ActionVlanVid(base.GenericStruct):
    """Action structure for OFPAT_SET_VLAN_VID

    .. note:: The vlan_vid field is 16 bits long,
              when an actual VLAN id is only 12 bits.
              The value 0xffff is used to indicate that no VLAN id was set

    :param type: OFPAT_SET_VLAN_PCP.
    :param length:     Length is 8.
    :param vlan_id:    VLAN priority.
    :param pad2:       Pad for bit alignment.
    """
    type = basic_types.UBInt16(ActionType.OFPAT_SET_VLAN_PCP,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    vlan_id = basic_types.UBInt16()
    pad2 = basic_types.PAD(2)

    def __init__(self, vlan_id=None):
        super().__init__()
        self.vlan_id = vlan_id


class ActionVlanPCP(base.GenericStruct):
    """Action structure for OFPAT_SET_VLAN_PCP.

    .. note:: The vlan_pcp field is 8 bits long,
              but only the lower 3 bits have meaning.

    :param type: OFPAT_SET_VLAN_PCP.
    :param length:     Length is 8.
    :param vlan_pcp:   VLAN Priority.
    :param pad:        Pad for bit alignment.
    """
    type = basic_types.UBInt16(ActionType.OFPAT_SET_VLAN_PCP,
                               enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    vlan_pcp = basic_types.UBInt8()
    pad = basic_types.PAD(3)

    def __init__(self, vlan_pcp=None):
        super().__init__()
        self.vlan_pcp = vlan_pcp


class ActionDLAddr(base.GenericStruct):
    """Action structure for OFPAT_SET_DL_SRC/DST.

    # TODO: implement validation of OFPAT_SET_DL_SRC/DST
    :param dl_addr_type: OFPAT_SET_DL_SRC/DST.
    :param length:     Length is 16.
    :param dl_addr:    Ethernet address.
    :param pad:        Pad for bit alignment.
    """
    dl_addr_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(16)
    dl_addr = basic_types.HWAddress()
    pad = basic_types.PAD(6)

    def __init__(self, dl_addr_type=None, dl_addr=None):
        super().__init__()
        self.dl_addr_type = dl_addr_type
        self.dl_addr = dl_addr


class ActionNWAddr(base.GenericStruct):
    """Action structure for OFPAT_SET_NW_SRC/DST.

    # TODO: implement validation of OFPAT_SET_TW_SRC/DST
    :param nw_addr_type: OFPAT_SET_TW_SRC/DST.
    :param length:       Length is 8.
    :param nw_addr:      IP Address
    """
    nw_addr_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    nw_addr = basic_types.UBInt32()

    def __init__(self, nw_addr_type=None, nw_addr=None):
        super().__init__()
        self.nw_addr_type = nw_addr_type
        self.nw_addr = nw_addr


class ActionNWTos(base.GenericStruct):
    """Action structure for OFPAT_SET_NW_TOS.

    .. note:: The nw_tos field is the 6 upper bits of the ToS field to set,
              in the original bit positions (shifted to the left by 2).

    # TODO: implement validation of OFPAT_SET_TW_SRC/DST
    :param nw_tos_type: OFPAT_SET_TW_SRC/DST.
    :param length:      Length is 8.
    :param nw_tos:      IP ToS (DSCP field, 6 bits).
    #                   TODO: Implement IPAddr field
    :param pad:         Pad for bit alignment.
    """
    nw_tos_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    nw_tos = basic_types.UBInt8()
    # TODO: Implement IPAddr field
    pad = basic_types.PAD(3)

    def __init__(self, nw_tos_type=None, nw_tos=None):
        super().__init__()
        self.nw_tos_type = nw_tos_type
        self.nw_tos = nw_tos


class ActionTPPort(base.GenericStruct):
    """Action structure for OFPAT_SET_TP_SRC/DST.

    # TODO: implement validation of OFPAT_SET_TP_SRC/DST
    :param tp_port_type: OFPAT_SET_TP_SRC/DST.
    :param length:     Length is 8.
    :param tp_port:    TCP/UDP/other port to set.
    :param pad:        Pad for bit alignment.
    """
    tp_port_type = basic_types.UBInt16(enum_ref=ActionType)
    length = basic_types.UBInt16(8)
    tp_port = basic_types.UBInt16()
    pad = basic_types.PAD(2)

    def __init__(self, tp_port_type=None, tp_port=None):
        super().__init__()
        self.tp_port_type = tp_port_type
        self.tp_port = tp_port


class ActionVendorHeader(base.GenericStruct):
    """Action header for OFPAT_VENDOR.

    The rest of the body is vendor-defined.

    :param type: OFPAT_VENDOR.
    :param length:     Length is a multiple of 8  # TODO: validate length
    :param vendor:     Vendor ID, which takes the same form as in VendorHeader
    """
    type = basic_types.UBInt16(ActionType.OFPAT_VENDOR,
                               enum_ref=ActionType)
    length = basic_types.UBInt16()
    vendor = basic_types.UBInt32()

    def __init__(self, length=None, vendor=None):
        super().__init__()
        self.length = length
        self.vendor = vendor
