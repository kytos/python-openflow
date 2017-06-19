"""The controller has requested to be notified when flows time out."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8, UBInt16, UBInt32, UBInt64
# Local source tree imports
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.header import Header, Type

__all__ = ('FlowRemoved', 'FlowRemovedReason')

# Enums


class FlowRemovedReason(IntEnum):
    """Why the flow was removed."""

    #: Flow idle time exceeded idle_timeout
    OFPRR_IDLE_TIMEOUT = 0
    #: Time exceeded hard_timeout
    OFPRR_HARD_TIMEOUT = 1
    #: Evicted by a DELETE flow mod
    OFPRR_DELETE = 2


# Classes
class FlowRemoved(GenericMessage):
    """Flow removed (datapath -> controller)."""

    #: :class:`~pyof.v0x01.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_FLOW_REMOVED)
    #: :class:`~pyof.v0x01.common.flow_match.Match`: OpenFlow Header
    match = Match()
    cookie = UBInt64()

    priority = UBInt16()
    reason = UBInt8(enum_ref=FlowRemovedReason)
    #: Align to 32-bits.
    pad = Pad(1)

    duration_sec = UBInt32()
    duration_nsec = UBInt32()

    idle_timeout = UBInt16()
    #: Align to 64-bits.
    pad2 = Pad(2)
    packet_count = UBInt64()
    byte_count = UBInt64()

    def __init__(self, xid=None, match=None, cookie=None, priority=None,
                 reason=None, duration_sec=None, duration_nsec=None,
                 idle_timeout=None, packet_count=None, byte_count=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): OpenFlow Header's xid.
            match (~pyof.v0x01.common.flow_match.Match): Fields' description.
            cookie (int): Opaque controller-issued identifier.
            priority (int): Priority level of flow entry.
            reason (~pyof.v0x01.asynchronous.flow_removed.FlowRemovedReason):
                Why the flow was removed.
            duration_sec (int): Time the flow was alive in seconds.
            duration_nsec (int): Time the flow was alive in nanoseconds in
                addition to duration_sec.
            idle_timeout (int): Idle timeout from original flow mod.
            packet_count (int): Number of packets.
            byte_count (int): Byte count.
        """
        super().__init__(xid)
        self.match = match
        self.cookie = cookie
        self.priority = priority
        self.reason = reason
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.idle_timeout = idle_timeout
        self.packet_count = packet_count
        self.byte_count = byte_count
