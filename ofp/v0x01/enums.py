class OFPType(object):
    """
    Message Type
    """
    # Symetric/Immutable messages
    OFPT_HELLO = 0
    OFPT_ERROR = 1
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_VENDOR = 4
    
    # Switch configuration messages
    # Controller/Switch messages
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_GET_CONFIG_REQUEST = 7
    OFPT_GET_CONFIG_REPLY = 8
    OFPT_SET_CONFIG = 9

    # Async messages
    OFPT_PACKET_IN = 10
    OFPT_FLOW_REMOVED = 11 
    OFPT_PORT_STATUS = 12

    # Controller command messages
    # Controller/switch message
    OFPT_PACKET_OUT = 13
    OFPT_FLOW_MOD = 14
    OFPT_PORT_MOD = 15

    # Statistics messages
    # Controller/Switch message
    OFPT_STATS_REQUEST = 16
    OFPT_STATS_REPLY = 17

    # Barrier messages
    # Controller/Switch message
    OFPT_BARRIER_REQUEST = 18
    OFPT_BARRIER_REPLY = 19

    # Queue Configuration messages
    # Controller/Switch message
    OFPT_QUEUE_GET_CONFIG_REQUEST = 20
    OFPT_QUEUE_GET_CONFIG_REPLY = 21


class OFPPortConfig(object):
    """
    Flags to indicate behavior of the physical port. These flags are used in
    OFPPhyPort to describe the current configuration. They are used in the
    OFPPortMod message to configure the port’s behavior.
    """

    OFPPC_PORT_DOWN = 1 << 0    # Port is administratively down
    OFPPC_NO_STP = 1 << 1       # Disable 802.1D spanning tree on port
    OFPPC_NO_RECV = 1 << 2      # Drop all packets except 802.1D spanning tree
    OFPPC_NO_RECV_STP = 1 << 3  # Drop received 802.1D STP packets
    OFPPC_NO_FLOOD = 1 << 4     # Do not include this port when flooding
    OFPPC_NO_FWD = 1 << 5       # Drop packets forwarded to port
    OFPPC_NO_PACKET_IN = 1 << 6 # Do not send packet-in msgs for port


class OFPPortState(object):
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
