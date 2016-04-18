"""Defines physical port classes and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ..foundation import base
from ..foundation import basic_types

# Enums


class OFPPortConfig(enum.Enum):
    """Flags to indicate behavior of the physical port.

    These flags are used in OFPPhyPort to describe the current configuration.
    They are used in the OFPPortMod message to configure the port's behavior.

    Enums:
        OFPPC_PORT_DOWN         # Port is administratively down.
        OFPPC_NO_RECV           # Drop all packets except 802.1D spanning tree.
        OFPPC_NO_FWD            # Drop packets forwarded to port.
        OFPPC_NO_PACKET_IN      # Do not send packet-in msgs for port.

        # Not 1.1
        OFPPC_NO_STP            # Disable 802.1D spanning tree on port.
        OFPPC_NO_RECV_STP       # Drop received 802.1D STP packets.
        OFPPC_NO_FLOOD          # Do not include this port when flooding.

    """

    OFPPC_PORT_DOWN = 1 << 0
    OFPPC_NO_RECV = 1 << 2
    OFPPC_NO_FWD = 1 << 5
    OFPPC_NO_PACKET_IN = 1 << 6


class OFPPortState(enum.Enum):
    """Current state of the physical port.

    These are not configurable from the controller.

    The OFPPS_STP_* bits have no effect on switch operation. The controller
    must adjust OFPPC_NO_RECV, OFPPC_NO_FWD, and OFPPC_NO_PACKET_IN
    appropriately to fully implement an 802.1D spanning tree.

    Enums:
        OFPPS_LINK_DOWN     # No physical link present.
        OFPPS_BLOCKED       # Port is blocked.
        OFPPS_LIVE          # Live for Fast Failover Group.

        Not 1.1
        OFPPS_LINK_DOWN     # Not learning or relaying frames.
        OFPPS_STP_LEARN     # Learning but not relaying frames.
        OFPPS_STP_FORWARD   # Learning and relaying frames.
        OFPPS_STP_BLOCK     # Not part of spanning tree.
        OFPPS_STP_MASK      # Bit mask for OFPPS_STP_* values.
    """

    OFPPS_LINK_DOWN = 1 << 0
    OFPPS_BLOCKED = 1 << 1
    OFPPS_LIVE = 1 << 2


class OFPPortNo(enum.Enum):
    """Port numbering. Physical ports are numbered starting from 1.

    Enums:
        OFPP_MAX            # Maximum number of physical switch ports.
        OFPP_IN_PORT        # Send the packet out the input port. This
                            # virtual port must be explicitly used
                            # in order to send back out of the input port.

        OFPP_TABLE          # Perform actions in flow table.
                            # NB: This can only be the destination
                            # port for packet-out messages

        OFPP_NORMAL         # Process with normal L2/L3 switching.
        OFPP_FLOOD          # All physical ports except input port and
                            # those disabled by STP
        OFPP_ALL            # All physical ports except input port
        OFPP_CONTROLLER     # Send to controller
        OFPP_LOCAL          # Local openflow "port"
        OFPP_NONE           # Not associated with a physical port
    """

    OFPP_MAX = 0xff00
    OFPP_IN_PORT = 0xfff8
    OFPP_TABLE = 0xfff9
    OFPP_NORMAL = 0xfffa
    OFPP_FLOOD = 0xfffb
    OFPP_ALL = 0xfffc
    OFPP_CONTROLLER = 0xfffd
    OFPP_LOCAL = 0xfffe

    # TODO: Strange... it should be ANY instead of NONE.
    OFPP_NONE = 0xffff


class OFPPortFeatures(enum.Enum):
    """Physical ports features.

    The curr, advertised, supported, and peer fields indicate link modes
    (10M to 10G full and half-duplex), link type (copper/fiber) and
    link features (autone-gotiation and pause).

    Enums:
        OFPPF_10MB_HD       # 10 Mb half-duplex rate support.
        OFPPF_10MB_FD       # 10 Mb full-duplex rate support.
        OFPPF_100MB_HD      # 100 Mb half-duplex rate support.
        OFPPF_100MB_FD      # 100 Mb full-duplex rate support.
        OFPPF_1GB_HD        # 1 Gb half-duplex rate support.
        OFPPF_1GB_FD        # 1 Gb full-duplex rate support.
        OFPPF_10GB_FD       # 10 Gb full-duplex rate support.
        OFPPF_40GB_FD       # 40 Gb full-duplex rate support.
        OFPPF_100GB_FD      # 100 Gb full-duplex rate support.
        OFPPF_1TB_FD        # 1 Tb full-duplex rate support.
        OFPPF_OTHER         # Other rate, not in the list.

        OFPPF_COPPER        # Copper medium.
        OFPPF_FIBER         # Fiber medium.
        OFPPF_AUTONEG       # Auto-negotiation.
        OFPPF_PAUSE         # Pause.
        OFPPF_PAUSE_ASYM    # Asymmetric pause.

    """

    OFPPF_10MB_HD = 1 << 0
    OFPPF_10MB_FD = 1 << 1
    OFPPF_100MB_HD = 1 << 2
    OFPPF_100MB_FD = 1 << 3
    OFPPF_1GB_HD = 1 << 4
    OFPPF_1GB_FD = 1 << 5
    OFPPF_10GB_FD = 1 << 6
    OFPPF_40GB_FD = 1 << 7
    OFPPF_100GB_FD = 1 << 8
    OFPPF_1TB_FD = 1 << 9
    OFPPF_OTHER = 1 << 10

    OFPPF_COPPER = 1 << 11
    OFPPF_FIBER = 1 << 12
    OFPPF_AUTONEG = 1 << 13
    OFPPF_PAUSE = 1 << 14
    OFPPF_PAUSE_ASYM = 1 << 15


# Classes (Structs)


class Port(base.GenericStruct):
    """
    Description of a physical port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    OFP_MAX_ETH_ALEN is 6. The name field is a null-terminated string
    containing a human-readable name for the interface. The value of
    OFP_MAX_PORT_NAME_LEN is 16.

        :param port_no
        :param hw_addr
        :param name
        :param config -- Bitmap of OFPPC* flags.
        :param state -- Bitmap of OFPPS* flags.

        # Bitmaps of OFPPF_* that describe features. All bits zeroed if
        # unsupported or unavailable.
        :param curr -- Current features.
        :param advertised -- Features being advertised by the port.
        :param supported -- Features supported by the port.
        :param peer -- Features advertised by peer.

    """
    _build_order = ('port_no', 'hw_addr', 'name', 'config', 'state', 'curr',
                    'advertised', 'supported', 'peer')

    # Attributes
    port_no = basic_types.UBInt16()
    hw_addr = basic_types.UBInt8Array(length=base.OFP_ETH_ALEN)
    name = basic_types.Char(length=base.OFP_MAX_PORT_NAME_LEN)
    config = basic_types.UBInt32()
    state = basic_types.UBInt32()

    curr = basic_types.UBInt32()
    advertised = basic_types.UBInt32()
    supported = basic_types.UBInt32()
    peer = basic_types.UBInt32()
    # TODO: Move code to version v0x02
    #curr_speed = basic_types.UBInt32()
    #max_speed = basic_types.UBInt32()

    def __init__(self, port_no=None, hw_addr=None, name=None, config=None,
                 state=None, curr=None, advertised=None, supported=None,
                 peer=None):

        self.port_no = port_no
        self.hw_addr = hw_addr
        self.name = name
        self.config = config
        self.state = state
        self.curr = curr
        self.advertised = advertised
        self.supported = supported
        self.peer = peer
        # TODO: Move code to version v0x02
        #self.curr_speed = curr_speed
        #self.max_speed = max_speed
