"""Defines physical port classes and related items."""

# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericStruct
from pyof.foundation.basic_types import (
    Char, FixedTypeList, HWAddress, UBInt16, UBInt32)
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN

# Third-party imports

__all__ = ('PhyPort', 'ListOfPhyPorts', 'Port', 'PortConfig', 'PortFeatures',
           'PortState')


class Port(IntEnum):
    """Port numbering.

    Physical ports are numbered starting from 1. Port number 0 is reserved by
    the specification and must not be used for a switch physical port.
    """

    #: Maximum number of physical switch ports.
    OFPP_MAX = 0xff00
    #: Send the packet out the input port. This virtual port must be explicitly
    #: used in order to send back out of the input port.
    OFPP_IN_PORT = 0xfff8
    #: Perform actions in flow table.
    #: NB: This can only be the destination port for packet-out messages
    OFPP_TABLE = 0xfff9
    #: Process with normal L2/L3 switching.
    OFPP_NORMAL = 0xfffa
    #: All physical ports except input port and those disabled by STP
    OFPP_FLOOD = 0xfffb
    #: All physical ports except input port
    OFPP_ALL = 0xfffc
    #: Send to controller
    OFPP_CONTROLLER = 0xfffd
    #: Local openflow "port"
    OFPP_LOCAL = 0xfffe
    #: Not associated with a physical port
    OFPP_NONE = 0xffff


class PortConfig(GenericBitMask):
    """Flags to indicate behavior of the physical port.

    These flags are used in OFPPhyPort to describe the current configuration.
    They are used in the OFPPortMod message to configure the port's behavior.
    """

    #: Port is administratively down.
    OFPPC_PORT_DOWN = 1 << 0
    #: Disable 802.1D spanning tree on port.
    OFPPC_NO_STP = 1 << 1
    #: Drop all packets except 802.1D spanning tree.
    OFPPC_NO_RECV = 1 << 2
    #: Drop received 802.1D STP packets.
    OFPPC_NO_RECV_STP = 1 << 3
    #: Do not include this port when flooding.
    OFPPC_FLOOD = 1 << 4
    #: Drop packets forwarded to port.
    OFPPC_NO_FWD = 1 << 5
    #: Do not send packet-in msgs for port.
    OFPPC_NO_PACKET_IN = 1 << 6


class PortFeatures(GenericBitMask):
    """Physical ports features.

    The :attr:`curr`, :attr:`advertised`, :attr:`supported`, and :attr:`peer`
    fields indicate link modes (10M to 10G full and half-duplex), link type
    (copper/fiber) and link features (autone-gotiation and pause).
    """

    #: 10 Mb half-duplex rate support.
    OFPPF_10MB_HD = 1 << 0
    #: 10 Mb full-duplex rate support.
    OFPPF_10MB_FD = 1 << 1
    #: 100 Mb half-duplex rate support.
    OFPPF_100MB_HD = 1 << 2
    #: 100 Mb full-duplex rate support.
    OFPPF_100MB_FD = 1 << 3
    #: 1 Gb half-duplex rate support.
    OFPPF_1GB_HD = 1 << 4
    #: 1 Gb full-duplex rate support.
    OFPPF_1GB_FD = 1 << 5
    #: 10 Gb full-duplex rate support.
    OFPPF_10GB_FD = 1 << 6
    #: Copper medium.
    OFPPF_COPPER = 1 << 7
    #: Fiber medium.
    OFPPF_FIBER = 1 << 8
    #: Auto-negotiation.
    OFPPF_AUTONEG = 1 << 9
    #: Pause.
    OFPPF_PAUSE = 1 << 10
    #: Asymmetric pause.
    OFPPF_PAUSE_ASYM = 1 << 11


class PortState(GenericBitMask):
    """Current state of the physical port.

    These are not configurable from the controller.

    The ``OFPPS_STP_*`` bits have no effect on switch operation. The controller
    must adjust :attr:`PortConfig.OFPPC_NO_RECV`,
    :attr:`~PortConfig.OFPPC_NO_FWD`, and
    :attr:`~PortConfig.OFPPC_NO_PACKET_IN` appropriately to fully implement an
    802.1D spanning tree.
    """

    #: Not learning or relaying frames.
    OFPPS_LINK_DOWN = 1 << 0
    #: Not learning or relaying frames.
    OFPPS_STP_LISTEN = 0 << 8
    #: Learning but not relaying frames.
    OFPPS_STP_LEARN = 1 << 8
    #: Learning and relaying frames.
    OFPPS_STP_FORWARD = 2 << 8
    #: Not part of spanning tree.
    OFPPS_STP_BLOCK = 3 << 8


# Classes


class PhyPort(GenericStruct):
    """Description of a physical port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    :data:`OFP_ETH_ALEN` is 6. The name field is a null-terminated string
    containing a human-readable name for the interface. The value of
    :data:`OFP_MAX_PORT_NAME_LEN` is 16.

    :attr:`curr`, :attr:`advertised`, :attr:`supported` and :attr:`peer` are
    bitmaps of :class:`~pyof.v0x01.common.phy_port.PortFeatures` enum values
    that describe features. If unsupported or unavailable, set all bits to
    zero.
    """

    port_no = UBInt16()
    hw_addr = HWAddress()
    name = Char(length=OFP_MAX_PORT_NAME_LEN)
    config = UBInt32(enum_ref=PortConfig)
    state = UBInt32(enum_ref=PortState)
    curr = UBInt32(enum_ref=PortFeatures)
    advertised = UBInt32(enum_ref=PortFeatures)
    supported = UBInt32(enum_ref=PortFeatures)
    peer = UBInt32(enum_ref=PortFeatures)

    def __init__(self, port_no=None, hw_addr=None, name=None, config=0,
                 state=PortState.OFPPS_STP_LISTEN, curr=0, advertised=0,
                 supported=0, peer=0):
        """Create a PhyPort with the optional parameters below.

        Args:
            port_no (int): Port number.
            hw_addr (HWAddress): Hardware address.
            name(str): Null-terminated name.
            config (~pyof.v0x01.common.phy_port.PortConfig):
                Bitmap of OFPPC* flags.
            state (~pyof.v0x01.common.phy_port.PortState):
                Bitmap of OFPPS* flags.
            curr (~pyof.v0x01.common.phy_port.PortFeatures): Current features.
            advertised (~pyof.v0x01.common.phy_port.PortFeatures):
                Features being advertised by the port.
            supported (~pyof.v0x01.common.phy_port.PortFeatures):
                Features supported by the port.
            peer (~pyof.v0x01.common.phy_port.PortFeatures):
                Features advertised by peer.
        """
        super().__init__()
        self.port_no = port_no
        self.hw_addr = hw_addr
        self.name = name
        self.config = config
        self.state = state
        self.curr = curr
        self.advertised = advertised
        self.supported = supported
        self.peer = peer


class ListOfPhyPorts(FixedTypeList):
    """List of PhyPorts.

    Represented by instances of PhyPort and used on
    :class:`pyof.v0x01.common.phy_port.FeaturesReply`/
    :class:`pyof.v0x01.controller2switch.features_reply.SwitchFeatures`
    objects.
    """

    def __init__(self, items=None):
        """Create a ListOfPhyPorts with the optional parameters below.

        Args:
            items (:class:`list`, :class:`PhyPort`): One :class:`PhyPort`
                instance or list.
        """
        super().__init__(pyof_class=PhyPort,
                         items=items)
