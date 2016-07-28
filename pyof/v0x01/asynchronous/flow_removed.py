"""The controller has requested to be notified when flows time out."""

# System imports
import enum

from pyof.v0x01.common import header as of_header
# Local source tree imports
from pyof.v0x01.common import flow_match
from pyof.v0x01.foundation import base, basic_types


# Third-party imports


__all__ = ('FlowRemoved', 'FlowRemovedReason')

# Enums


class FlowRemovedReason(enum.Enum):
    """Why the flow was removed."""

    #: Flow idle time exceeded idle_timeout
    OFPRR_IDLE_TIMEOUT = 1
    #: Time exceeded hard_timeout
    OFPRR_HARD_TIMEOUT = 2
    #: Evicted by a DELETE flow mod
    OFPRR_DELETE = 3


# Classes
class FlowRemoved(base.GenericMessage):
    """Flow removed (datapath -> controller)."""

    #: :class:`~.header.Header`: OpenFlow Header
    header = of_header.Header(message_type=of_header.Type.OFPT_FLOW_REMOVED)
    #: :class:`~.flow_match.Match`: OpenFlow Header
    match = flow_match.Match()
    cookie = basic_types.UBInt64()

    priority = basic_types.UBInt16()
    reason = basic_types.UBInt8(enum_ref=FlowRemovedReason)
    #: Align to 32-bits.
    pad = basic_types.PAD(1)

    duration_sec = basic_types.UBInt32()
    duration_nsec = basic_types.UBInt32()

    idle_timeout = basic_types.UBInt16()
    #: Align to 64-bits.
    pad2 = basic_types.PAD(2)
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()

    def __init__(self, xid=None, match=None, cookie=None, priority=None,
                 reason=None, duration_sec=None, duration_nsec=None,
                 idle_timeout=None, packet_count=None, byte_count=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): OpenFlow Header's xid.
            match (Match): Fields' description.
            cookie (int): Opaque controller-issued identifier.
            priority (int): Priority level of flow entry.
            reason (FlowRemovedReason): Why the flow was removed.
            duration_sec (int): Time the flow was alive in seconds.
            duration_nsec (int): Time the flow was alive in nanoseconds in
                addition to duration_sec.
            idle_timeout (int): Idle timeout from original flow mod.
            packet_count (int): Number of packets.
            byte_count (int): Byte count.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.match = match
        self.cookie = cookie
        self.priority = priority
        self.reason = reason
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.idle_timeout = idle_timeout
        self.packet_count = packet_count
        self.byte_count = byte_count
