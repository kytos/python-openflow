"""Defines physical port classes and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from foundation import base
from foundation import basic_types

# Enums

class OFPPortConfig(enum.Enum):
    """Flags to indicate behavior of the physical port.

    These flags are used in OFPPhyPort to describe the current configuration.
    They are used in the OFPPortMod message to configure the port's behavior.
    """

    OFPPC_PORT_DOWN = 1 << 0    # Port is administratively down
    # Not 1.1
    # OFPPC_NO_STP = 1 << 1       # Disable 802.1D spanning tree on port
    OFPPC_NO_RECV = 1 << 2      # Drop all packets except 802.1D spanning tree
    # Not 1.1
    # OFPPC_NO_RECV_STP = 1 << 3  # Drop received 802.1D STP packets
    # Not 1.1
    # OFPPC_NO_FLOOD = 1 << 4     # Do not include this port when flooding
    OFPPC_NO_FWD = 1 << 5       # Drop packets forwarded to port
    OFPPC_NO_PACKET_IN = 1 << 6 # Do not send packet-in msgs for port


class OFPPortState(enum.Enum):
    """Current state of the physical port.

    These are not configurable from the controller.

    The OFPPS_STP_* bits have no effect on switch operation. The controller must
    adjust OFPPC_NO_RECV, OFPPC_NO_FWD, and OFPPC_NO_PACKET_IN appropriately to
    fully implement an 802.1D spanning tree.
    """

    OFPPS_LINK_DOWN = 1 << 0    # No physical link present
    OFPPS_BLOCKED = 1 << 1      # Port is blocked
    OFPPS_LIVE = 1 <<2          # Live for Fast Failover Group
    # Not 1.1
    # OFPPS_STP_LISTEN = 0 << 8   # Not learning or relaying frames
    # OFPPS_STP_LEARN = 1 << 8    # Learning but not relaying frames
    # OFPPS_STP_FORWARD = 2 << 8  # Learning and relaying frames
    # OFPPS_STP_BLOCK = 3 << 8    # Not part of spanning tree
    # OFPPS_STP_MASK = 3 << 8     # Bit mask for OFPPS_STP_* values


class OFPPortNo(enum.Enum):
    """Port numbering. Physical ports are numbered starting from 1."""

    OFPP_MAX = 0xff00           # Maximum number of physical switch ports.

    # Fake output "ports"
    OFPP_IN_PORT = 0xfff8       # Send the packet out the input port. This
                                # virtual port must be explicitly used
                                # in order to send back out of the input port.

    OFPP_TABLE = 0xfff9         # Perform actions in flow table.
                                # NB: This can only be the destination
                                # port for packet-out messages

    OFPP_NORMAL = 0xfffa        # Process with normal L2/L3 switching.
    OFPP_FLOOD = 0xfffb         # All physical ports except input port and
                                # those disabled by STP

    OFPP_ALL = 0xfffc          # All physical ports except input port
    OFPP_CONTROLLER = 0xfffd    # Send to controller
    OFPP_LOCAL = 0xfffe         # Local openflow "port"

    #TODO: Strange... it should be ANY instead of NONE.
    OFPP_NONE = 0xffff          # Not associated with a physical port


class OFPPortFeatures(enum.Enum):
    """Physical ports features.

    The curr, advertised, supported, and peer fields indicate link modes
    (10M to 10G full and half-duplex), link type (copper/fiber) and
    link features (autone-gotiation and pause).
    """

    OFPPF_10MB_HD = 1 << 0      # 10 Mb half-duplex rate support
    OFPPF_10MB_FD = 1 << 1      # 10 Mb full-duplex rate support
    OFPPF_100MB_HD = 1 << 2     # 100 Mb half-duplex rate support
    OFPPF_100MB_FD = 1 << 3     # 100 Mb full-duplex rate support
    OFPPF_1GB_HD = 1 << 4       # 1 Gb half-duplex rate support
    OFPPF_1GB_FD = 1 << 5       # 1 Gb full-duplex rate support
    OFPPF_10GB_FD = 1 << 6      # 10 Gb full-duplex rate support
    OFPPF_40GB_FD = 1 << 7      # 40 Gb full-duplex rate support
    OFPPF_100GB_FD = 1 << 8     # 100 Gb full-duplex rate support
    OFPPF_1TB_FD = 1 << 9       # 1 Tb full-duplex rate support
    OFPPF_OTHER = 1 << 10       # Other rate, not in the list

    OFPPF_COPPER = 1 << 11      # Copper medium
    OFPPF_FIBER = 1 << 12       # Fiber medium
    OFPPF_AUTONEG = 1 << 13     # Auto-negotiation
    OFPPF_PAUSE = 1 << 14       # Pause
    OFPPF_PAUSE_ASYM = 1 << 15  # Asymmetric pause


# Classes (Structs)


class OFPPort(base.GenericStruct):
    """
    Description of a physical port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    OFP_MAX_ETH_ALEN is 6. The name field is a null-terminated string
    containing a human-readable name for the interface. The value of
    OFP_MAX_PORT_NAME_LEN is 16.
    """
    _build_order = ('port_no', 'hw_addr', 'name', 'config', 'state', 'curr',
                    'advertised', 'supported', 'peer')

    # Attributes
    port_no = basic_types.UBInt16()
    hw_addr = basic_types.UBInt8Array(length=base.OFP_ETH_ALEN)
    name = basic_types.Char(length=base.OFP_MAX_PORT_NAME_LEN)
    config = basic_types.UBInt32()      # Bitmap of OFPPC* flags
    state = basic_types.UBInt32()       # Bitmap of OFPPS* flags

    # Bitmaps of OFPPF_* that describe features. All bits zeroed if
    # unsupported or unavailable.
    curr = basic_types.UBInt32()        # Current features
    advertised = basic_types.UBInt32()  # Features being advertised by the port
    supported = basic_types.UBInt32()   # Features supported by the port
    peer = basic_types.UBInt32()        # Features advertised by peer

    curr_speed = basic_types.UBInt32()  # Current port bitrate in kbps
    max_speed = basic_types.UBInt32()   # Max port bitrate in kbps
