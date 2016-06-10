"""The controller has requested to be notified when flows time out"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import flow_match
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Enums


class FlowRemovedReason(enum.Enum):
    """
    Reason field enum

        OFPRR_IDLE_TIMEOUT      # Flow idle time exceeded idle_timeout
        OFPRR_HARD_TIMEOUT      # Time exceeded hard_timeout
        OFPRR_DELETE            # Evicted by a DELETE flow mod

    """
    OFPRR_IDLE_TIMEOUT = 1
    OFPRR_HARD_TIMEOUT = 2
    OFPRR_DELETE = 3


# Classes
class FlowRemoved(base.GenericMessage):
    """Flow removed (datapath -> controller).

    :param header:        Openflow Header
    :param match:         Description of Fields
    :param cookie:        Opaque controller-issued identifier
    :param priority:      Priority level of flow entry
    :param reason:        One of OFPRR_*
    :param pad:           Align to 32-bits
    :param duration_sec:  Time flow was alive in seconds
    :param duration_nsec: Time flow was alive in nanoseconds beyond
                          duration_sec
    :param idle_timeout:  Idle timeout from original flow mod
    :param pad2:          Align to 64-bits
    :param packet_count:  Number of packets
    :param byte_count:    Bytes count
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_FLOW_REMOVED)
    match = flow_match.Match()
    cookie = basic_types.UBInt64()

    priority = basic_types.UBInt16()
    reason = basic_types.UBInt8(enum_ref=FlowRemovedReason)
    pad = basic_types.PAD(1)

    duration_sec = basic_types.UBInt32()
    duration_nsec = basic_types.UBInt32()

    idle_timeout = basic_types.UBInt16()
    pad2 = basic_types.PAD(2)
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()

    def __init__(self, xid=None, match=None, cookie=None, priority=None,
                 reason=None, duration_sec=None, duration_nsec=None,
                 idle_timeout=None, packet_count=None, byte_count=None):
        super().__init__()
        self.header.xid = xid
        self.match = match
        self.cookie = cookie
        self.priority = priority
        self.reason = reason
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.idle_timeout = idle_timeout
        self.packet_count = packet_count
        self.byte_count = byte_count
