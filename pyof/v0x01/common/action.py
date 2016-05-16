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
    """
    Defines the Header that is common to all actions.

        :param action_type: One of OFPAT_.
        :param length:     Length of action, including this header.
        :param pad:        Pad for 64-bit alignment.
    """
    action_type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    pad = basic_types.PAD(4)

    def __init__(self, action_type=None, length=None):
        self.action_type = action_type
        self.length = length


class ActionOutput(base.GenericStruct):
    """Defines the actions output.

        :param type: OFPAT_OUTPUT.
        :param length:     Length is 8.
        :param port:       Output port.
        :param max_length: Max length to send to controller.
    """
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    port = basic_types.UBInt16()
    max_length = basic_types.UBInt16()

    def __init__(self, length=None, port=None,
                 max_length=None):
        self.type = ActionType.OFPAT_OUTPUT
        self.length = length
        self.port = port
        self.max_length = max_length


class ActionEnqueue(base.GenericStruct):
    """
    A switch may support only queues that are tied to specific PCP/TOS bits.
    In that case, we cannot map an arbitrary flow to a specific queue,
    therefore the action ENQUEUE is not supported. The user can still use
    these queues and map flows to them by setting the relevant fields
    (TOS, VLAN PCP).

        :param type: OFPAT_ENQUEUE.
        :param length:     Len is 16
        :param port:       Port that queue belongs. Should refer to a valid
                           physical port.
                           (i.e. < OFPP_MAX) or OFPP_IN_PORT
        :param pad:        Pad for 64-bit alignment.
        :param queue_id:   Where to enqueue the packets.
    """
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    port = basic_types.UBInt16()
    pad = basic_types.PAD(6)
    queue_id = basic_types.UBInt32()

    def __init__(self, length=None, port=None, queue_id=None):
        self.type = ActionType.OFPAT_ENQUEUE
        self.length = length
        self.port = port
        self.queue_id = queue_id


class ActionVlanVid(base.GenericStruct):
    """Action structure for OFPAT_SET_VLAN_VID

        :param type: OFPAT_SET_VLAN_PCP.
        :param length:     Length is 8.
        :param vlan_id:    VLAN priority.
        :param pad2:       Pad for bit alignment.
    """
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    vlan_id = basic_types.UBInt16()
    pad2 = basic_types.PAD(2)

    def __init__(self, length=None, vlan_id=None):
        self.type = ActionType.OFPAT_SET_VLAN_PCP
        self.length = length
        self.vlan_id = vlan_id


class ActionVlanPCP(base.GenericStruct):
    """Action structure for OFPAT_SET_VLAN_PCP.

        :param type: OFPAT_SET_VLAN_PCP.
        :param length:     Length is 8.
        :param vlan_pcp:   VLAN Priority.
        :param pad:        Pad for bit alignment.
    """
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    vlan_pcp = basic_types.UBInt8()
    pad = basic_types.PAD(3)

    def __init__(self, length=None, vlan_pcp=None):
        self.type = ActionType.OFPAT_SET_VLAN_PCP
        self.length = length
        self.vlan_pcp = vlan_pcp


class ActionDLAddr(base.GenericStruct):
    """Action structure for OFPAT_SET_DL_SRC/DST.

        :param dl_addr_type: OFPAT_SET_DL_SRC/DST.
        :param length:     Length is 16.
        :param dl_addr:    Ethernet address.
        :param pad:        Pad for bit alignment.
    """
    dl_addr_type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    dl_addr = basic_types.UBInt8Array(length=base.OFP_ETH_ALEN)
    pad = basic_types.PAD(6)

    def __init__(self, dl_addr_type=None, length=None, dl_addr=None):
        self.dl_addr_type = dl_addr_type
        self.length = length
        self.dl_addr = dl_addr


class ActionNWAddr(base.GenericStruct):
    """Action structure for OFPAT_SET_NW_SRC/DST.

        :param nw_addr_type: OFPAT_SET_TW_SRC/DST.
        :param length:     Length is 8.
        :param nw_addr:    IP Address
    """
    nw_addr_type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    nw_addr = basic_types.UBInt32()

    def __init__(self, nw_addr_type=None, length=None, nw_addr=None):
        self.nw_addr_type = nw_addr_type
        self.length = length
        self.nw_addr = nw_addr


class ActionNWTos(base.GenericStruct):
    """Action structure for OFPAT_SET_NW_TOS.

        :param nw_tos_type: OFPAT_SET_TW_SRC/DST.
        :param length:     Length is 8.
        :param nw_tos:     IP ToS (DSCP field, 6 bits).
        :param pad:        Pad for bit alignment.
    """
    nw_tos_type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    nw_tos = basic_types.UBInt8()
    pad = basic_types.PAD(3)

    def __init__(self, nw_tos_type=None, length=None, nw_tos=None):
        self.nw_tos_type = nw_tos_type
        self.length = length
        self.nw_tos = nw_tos


class ActionTPPort(base.GenericStruct):
    """Action structure for OFPAT_SET_TP_SRC/DST.

        :param tp_port_type: OFPAT_SET_TP_SRC/DST.
        :param length:     Length is 8.
        :param tp_port:    TCP/UDP port.
        :param pad:        Pad for bit alignment.
    """
    tp_port_type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    tp_port = basic_types.UBInt16()
    pad = basic_types.PAD(2)

    def __init__(self, tp_port_type=None, length=None, tp_port=None):
        self.tp_port_type = tp_port_type
        self.length = length
        self.tp_port = tp_port


class ActionVendorHeader(base.GenericStruct):
    """Action header for OFPAT_VENDOR.
    The rest of the body is vendor-defined.

        :param type: OFPAT_VENDOR.
        :param length:     Length is a multiple of 8.
        :param vendor:     Vendor ID, which takes the same form as in "struct
                           ofp_vendor_header".
    """
    type = basic_types.UBInt16()
    length = basic_types.UBInt16()
    vendor = basic_types.UBInt32()

    def __init__(self, length=None, vendor=None):

        self.type = ActionType.OFPAT_VENDOR
        self.length = length
        self.vendor = vendor
