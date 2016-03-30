from enum import Enum

class OFPPortConfig(Enum):
    """
    Flags to indicate behavior of the physical port. These flags are used in
    OFPPhyPort to describe the current configuration. They are used in the
    OFPPortMod message to configure the port's behavior.
    """

    OFPPC_PORT_DOWN = 1 << 0    # Port is administratively down
    OFPPC_NO_STP = 1 << 1       # Disable 802.1D spanning tree on port
    OFPPC_NO_RECV = 1 << 2      # Drop all packets except 802.1D spanning tree
    OFPPC_NO_RECV_STP = 1 << 3  # Drop received 802.1D STP packets
    OFPPC_NO_FLOOD = 1 << 4     # Do not include this port when flooding
    OFPPC_NO_FWD = 1 << 5       # Drop packets forwarded to port
    OFPPC_NO_PACKET_IN = 1 << 6 # Do not send packet-in msgs for port


class OFPPortState(Enum):
    """
    Current state of the physical port. These are not configurable from the
    controller.

    The OFPPS_STP_* bits have no effect on switch operation. The controller must
    adjust OFPPC_NO_RECV, OFPPC_NO_FWD, and OFPPC_NO_PACKET_IN appropriately to
    fully implement an 802.1D spanning tree.
    """

    OFPPS_LINK_DOWN = 1 << 0    # No physical link present.
    OFPPS_STP_LISTEN = 0 << 8   # Not learning or relaying frames.
    OFPPS_STP_LEARN = 1 << 8    # Learning but not relaying frames.
    OFPPS_STP_FORWARD = 2 << 8  # Learning and relaying frames.
    OFPPS_STP_BLOCK = 3 << 8    # Not part of spanning tree.
    OFPPS_STP_MASK = 3 << 8     # Bit mask for OFPPS_STP_* values.


class OFPPort(Enum):
    """
    Port numbering. Physical ports are numbered starting from 1.
    """

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

    OFPP_ALL =  0xfffc          # All physical ports except input port
    OFPP_CONTROLLER = 0xfffd    # Send to controller
    OFPP_LOCAL = 0xfffe         # Local openflow "port"
    OFPP_NONE = 0xffff          # Not associated with a physical port


class OFPPortFeatures(Enum):
    """
    Physical ports features.

    The curr, advertised, supported, and peer fields indicate link modes (10M
    to 10G full and half-duplex), link type (copper/fiber) and link features
    (autone-gotiation and pause).
    """

    OFPPF_10MB_HD = 1 << 0      # 10 Mb half-duplex rate support.
    OFPPF_10MB_FD = 1 << 1      # 10 Mb full-duplex rate support.
    OFPPF_100MB_HD = 1 << 2     # 100 Mb half-duplex rate support.
    OFPPF_100MB_FD = 1 << 3     # 100 Mb full-duplex rate support.
    OFPPF_1GB_HD = 1 << 4       # 1 Gb half-duplex rate support.
    OFPPF_1GB_FD = 1 << 5       # 1 Gb full-duplex rate support.
    OFPPF_10GB_FD = 1 << 6      # 10 Gb full-duplex rate support.
    OFPPF_COPPER = 1 << 7       # Copper medium.
    OFPPF_FIBER = 1 << 8        # Fiber medium.
    OFPPF_AUTONEG = 1 << 9      # Auto-negotiation.
    OFPPF_PAUSE = 1 << 10       # Pause.
    OFPPF_PAUSE_ASYM = 1 << 11  # Asymmetric pause.


class OFPFlowWildcards(Enum):
    """
    If no wildcards are set, then the ofp_match exactly describes a flow, over
    the entire OpenFlow 12-tuple. On the other extreme, if all the wildcard
    flags are set, then every flow will match.

    The source and destination netmasks are each specified with a 6-bit number
    in the wildcard description. It is interpreted similar to the CIDR suffix,
    but with the opposite meaning, since this is being used to indicate which
    bits in the IP address should be treated as "wild". For example, a CIDR
    suffix of "24" means to use a netmask of "255.255.255.0". However, a
    wildcard mask value of "24" means that the least-significant 24-bits are
    wild, so it forms a netmask of "255.0.0.0".
    """

    OFPFW_IN_PORT = 1 << 0          # Switch input port
    OFPFW_DL_VLAN = 1 << 1          # VLAN ID
    OFPFW_DL_SRC = 1 << 2           # Ethernet source mac
    FPFW_DL_DST = 1 << 3            # Ethernet dst mac
    OFPFW_DL_TYPE = 1 << 4          # Ethernet frame type
    OFPFW_NW_PROTO = 1 << 5         # IP Protocol
    OFPFW_TP_SRC = 1 << 6           # TCP/UDP source port
    OFPFW_TP_DST = 1 << 7           # TCP/UDP dst port

    # IP source address wildcard bit count. 0 is exact match, 1 ignores the
    # LSB, 2 ignores the 2 least-significant bits, ..., 32 and higher wildcard
    # the entire field. This is the *opposite* of the usual convention where
    # e.g. /24 indicates that 8 bits (not 24 bits) are wildcarded.
    OFPFW_NW_SRC_SHIFT = 8
    OFPFW_NW_SRC_BITS = 6
    OFPFW_NW_SRC_MASK = ((1 << OFPFW_NW_SRC_BITS) - 1) << OFPFW_NW_SRC_SHIFT
    OFPFW_NW_SRC_ALL = 32 << OFPFW_NW_SRC_SHIFT

    # IP destination address wildcard bit count. Same format as source.
    OFPFW_NW_DST_SHIFT = 14
    OFPFW_NW_DST_BITS = 6
    OFPFW_NW_DST_MASK = ((1 << OFPFW_NW_DST_BITS) - 1) << OFPFW_NW_DST_SHIFT
    OFPFW_NW_DST_ALL = 32 << OFPFW_NW_DST_SHIFT

    OFPFW_DL_VLAN_PCP = 1 << 20     # VLAN priority.
    OFPFW_NW_TOS = 1 << 21,         # IP ToS (DSCP field, 6 bits).

    OFPFW_ALL = ((1 << 22) - 1)     # Wildcard all fields


class OFPActionType(Enum):
    """
    A number of actions may be associated with flows or packets. The currently
    defined action types are:
    """

    OFPAT_OUTPUT = 0        # Output to switch port.
    OFPAT_SET_VLAN_VID = 1  # Set the 802.1q VLAN id.
    OFPAT_SET_VLAN_PCP = 2  # Set the 802.1q priority.
    OFPAT_STRIP_VLAN = 3    # Strip the 802.1q header.
    OFPAT_SET_DL_SRC = 4    # Ethernet source address.
    OFPAT_SET_DL_DST = 5    # Ethernet destination address.
    OFPAT_SET_NW_SRC = 6    # IP source address.
    OFPAT_SET_NW_DST = 7    # IP destination address.
    OFPAT_SET_NW_TOS = 8    # IP ToS (DSCP field, 6 bits).
    OFPAT_SET_TP_SRC = 9    # TCP/UDP source port.
    OFPAT_SET_TP_DST = 10   # TCP/UDP destination port.
    OFPAT_ENQUEUE = 11      # Output to queue.
    OFPAT_VENDOR = 0xffff
