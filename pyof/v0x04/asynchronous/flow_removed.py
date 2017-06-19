"""The controller has requested to be notified when flows time out."""
# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import UBInt8, UBInt16, UBInt32, UBInt64
# Local source tree imports
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header, Type

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
    #: Group was removed.
    OFPRR_GROUP_DELETE = 3


# Classes


class FlowRemoved(GenericMessage):
    """Flow removed (datapath -> controller).

    If the controller has requested to be notified when flow entries time out
    or are deleted from tables, the datapath does this with the
    OFPT_FLOW_REMOVED message.
    """

    #: :class:`~pyof.v0x04.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_FLOW_REMOVED)
    #: Opaque controller-issued identifier.
    cookie = UBInt64()
    #: Priority level of flow entry.
    priority = UBInt16()
    #: One of OFPRR_*.
    reason = UBInt8(enum_ref=FlowRemovedReason)
    #: ID of the table
    table_id = UBInt8()
    #: Time flow was alive in seconds.
    duration_sec = UBInt32()
    #: Time flow was alive in nanoseconds beyond duration_sec.
    duration_nsec = UBInt32()
    #: Idle timeout from original flow mod.
    idle_timeout = UBInt16()
    #: Hard timeout from original flow mod.
    hard_timeout = UBInt16()
    packet_count = UBInt64()
    byte_count = UBInt64()
    #: Description of fields. Variable size.
    #: :class:`~pyof.v0x04.common.flow_match.Match`
    match = Match()

    def __init__(self, xid=None, cookie=None, priority=None, reason=None,
                 table_id=None, duration_sec=None, duration_nsec=None,
                 idle_timeout=None, hard_timeout=None, packet_count=None,
                 byte_count=None, match=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): OpenFlow Header's xid.
            cookie (int): Opaque controller-issued identifier.
            priority (int): Priority level of flow entry.
            reason (~pyof.v0x04.asynchronous.flow_removed.FlowRemovedReason):
                Why the flow was removed.
            table_id (int): ID of the table.
            duration_sec (int): Time the flow was alive in seconds.
            duration_nsec (int): Time the flow was alive in nanoseconds in
                addition to duration_sec.
            idle_timeout (int): Idle timeout from original flow mod.
            hard_timeout (int): Hard timeout from original flow mod.
            packet_count (int): Number of packets.
            byte_count (int): Byte count.
            match (~pyof.v0x04.common.flow_match.Match): Fields' description.
        """
        super().__init__(xid)
        self.cookie = cookie
        self.priority = priority
        self.reason = reason
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.match = match
