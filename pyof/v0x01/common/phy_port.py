"""Defines physical port classes and related items"""

# System imports
import enum
# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class Port(enum.Enum):
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


class PortConfig(base.GenericBitMask):
    """Flags to indicate behavior of the physical port.

    These flags are used in OFPPhyPort to describe the current configuration.
    They are used in the OFPPortMod message to configure the port's behavior.

        OFPPC_PORT_DOWN     # Port is administratively down.
        OFPPC_NO_STP        # Disable 802.1D spanning tree on port.
        OFPPC_NO_RECV       # Drop all packets except 802.1D spanning tree.
        OFPPC_NO_RECV_STP   # Drop received 802.1D STP packets.
        OFPPC_NO_FLOOD      # Do not include this port when flooding.
        OFPPC_NO_FWD        # Drop packets forwarded to port.
        OFPPC_NO_PACKET_IN  # Do not send packet-in msgs for port.
    """
    OFPC_PORT_DOWN = 1 << 0
    OFPPC_NO_STP = 1 << 1
    OFPPC_NO_RECV = 1 << 2
    OFPPC_NO_RECV_STP = 1 << 3
    OFPPC_FLOOD = 1 << 4
    OFPPC_NO_FWD = 1 << 5
    OFPPC_NO_PACKET_IN = 1 << 6


class PortFeatures(base.GenericBitMask):
    """Physical ports features.

    The curr, advertised, supported, and peer fields indicate link modes
    (10M to 10G full and half-duplex), link type (copper/fiber) and
    link features (autone-gotiation and pause).

        OFPPF_10MB_HD     # 10 Mb half-duplex rate support.
        OFPPF_10MB_FD     # 10 Mb full-duplex rate support.
        OFPPF_100MB_HD    # 100 Mb half-duplex rate support.
        OFPPF_100MB_FD    # 100 Mb full-duplex rate support.
        OFPPF_1GB_HD      # 1 Gb half-duplex rate support.
        OFPPF_1GB_FD      # 1 Gb full-duplex rate support.
        OFPPF_COPPER      # Copper medium.
        OFPPF_FIBER       # Fiber medium.
        OFPPF_AUTONEG     # Auto-negotiation.
        OFPPF_PAUSE       # Pause.
        OFPPF_PAUSE_ASYM  # Asymmetric pause.
    """
    OFPPF_10MB_HD = 1 << 0
    OFPPF_10MB_FD = 1 << 1
    OFPPF_100MB_HD = 1 << 2
    OFPPF_100MB_FD = 1 << 3
    OFPPF_1GB_HD = 1 << 4
    OFPPF_1GB_FD = 1 << 5
    OFPPF_10GB_FD = 1 << 6
    OFPPF_COPPER = 1 << 11
    OFPPF_FIBER = 1 << 12
    OFPPF_AUTONEG = 1 << 13
    OFPPF_PAUSE = 1 << 14
    OFPPF_PAUSE_ASYM = 1 << 15


class PortState(base.GenericBitMask):
    """Current state of the physical port.

    These are not configurable from the controller.

    The OFPPS_STP_* bits have no effect on switch operation. The controller
    must adjust OFPPC_NO_RECV, OFPPC_NO_FWD, and OFPPC_NO_PACKET_IN
    appropriately to fully implement an 802.1D spanning tree.

        OFPPS_LINK_DOWN    # Not learning or relaying frames.
        OFPPS_STP_LISTEN   # Not learning or relaying frames.
        OFPPS_STP_LEARN    # Learning but not relaying frames.
        OFPPS_STP_FORWARD  # Learning and relaying frames.
        OFPPS_STP_BLOCK    # Not part of spanning tree.
        OFPPS_STP_MASK     # Bit mask for OFPPS_STP_* values.
    """
    OFPPS_LINK_DOWN = 1 << 0
    OFPPS_STP_LISTEN = 0 << 8
    OFPPS_STP_LEARN = 1 << 8
    OFPPS_STP_FORWARD = 2 << 8
    OFPPS_STP_BLOCK = 3 << 8
    # OFPPS_STP_MASK = 3 << 8  - Refer to ISSUE #7


# Classes


class PhyPort(base.GenericStruct):
    """Description of a physical port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    OFP_MAX_ETH_ALEN is 6. The name field is a null-terminated string
    containing a human-readable name for the interface. The value of
    OFP_MAX_PORT_NAME_LEN is 16.

    :param port_no
    :param hw_addr
    :param name:       Null-terminated
    :param config:     Bitmap of OFPPC* flags.
    :param state:      Bitmap of OFPPS* flags.

    # Bitmaps of OFPPF_* that describe features. All bits zeroed if
    # unsupported or unavailable.
    :param curr:       Current features.
    :param advertised: Features being advertised by the port.
    :param supported:  Features supported by the port.
    :param peer:       Features advertised by peer.
    """
    port_no = basic_types.UBInt16()
    hw_addr = basic_types.HWAddress()
    name = basic_types.Char(length=base.OFP_MAX_PORT_NAME_LEN)
    config = basic_types.UBInt32(enum_ref=PortConfig)
    state = basic_types.UBInt32(enum_ref=PortState)
    curr = basic_types.UBInt32(enum_ref=PortFeatures)
    advertised = basic_types.UBInt32(enum_ref=PortFeatures)
    supported = basic_types.UBInt32(enum_ref=PortFeatures)
    peer = basic_types.UBInt32(enum_ref=PortFeatures)

    def __init__(self, port_no=None, hw_addr=None, name=None, config=None,
                 state=None, curr=None, advertised=None, supported=None,
                 peer=None):
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


class ListOfPhyPorts(basic_types.FixedTypeList):
    """List of PhyPorts.

    Represented by instances of PhyPort and
    used on FeaturesReply/SwitchFeatures objects

    :param items: (optional) Instance or a list of instances of PhyPort
    """
    def __init__(self, items=None):
        super().__init__(pyof_class=PhyPort,
                         items=items)
