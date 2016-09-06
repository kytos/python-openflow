"""For packets received by the datapath and sent to the controller."""

# System imports
from enum import Enum

from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header, Type
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import (BinaryData, Pad, UBInt8, UBInt16,
                                         UBInt32, UBInt64)

# Third-party imports


__all__ = ('PacketIn', 'PacketInReason')

# Enums


class PacketInReason(Enum):
    """Reason why this packet is being sent to the controller."""

    #: No matching flow
    OFPR_NO_MATCH = 0
    #: Action explicitly output to controller
    OFPR_ACTION = 1


# Classes


class PacketIn(GenericMessage):
    """Packet received on port (datapath -> controller)."""

    #: :class:`~.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_PACKET_IN)
    buffer_id = UBInt32()
    total_len = UBInt16()
    reason = UBInt8(enum_ref=PacketInReason)
    table_id = UBInt8()
    cookie = UBInt64()
    match = Match()
    pad = Pad(2)
    data = BinaryData()

    def __init__(self, xid=None, buffer_id=None, total_len=None, reason=None,
                 table_id=None, cookie=None, data=b''):

        """Assign parameters to object attributes.

        Args:
            xid (int): Header's xid.
            buffer_id (int): ID assigned by datapath.
            total_len (int): Full length of frame.
            reason (PacketInReason): The reason why the packet is being sent
            table_id (int): ID of the table that was looked up
            cookie (int): Cookie of the flow entry that was looked up
            data (bytes): Ethernet frame, halfway through 32-bit word, so the
                IP header is 32-bit aligned. The amount of data is inferred
                from the length field in the header. Because of padding,
                offsetof(struct ofp_packet_in, data) ==
                sizeof(struct ofp_packet_in) - 2.
        """
        super().__init__(xid)
        self.buffer_id = buffer_id
        self.total_len = total_len
        self.reason = reason
        self.table_id = table_id
        self.cookie = cookie
        self.data = data
