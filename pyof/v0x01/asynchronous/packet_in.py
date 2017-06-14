"""For packets received by the datapath and sent to the controller."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import (
    BinaryData, Pad, UBInt8, UBInt16, UBInt32)
from pyof.v0x01.common.constants import NO_BUFFER
from pyof.v0x01.common.header import Header, Type

# Third-party imports


__all__ = ('PacketIn', 'PacketInReason')

# Enums


class PacketInReason(IntEnum):
    """Reason why this packet is being sent to the controller."""

    #: No matching flow
    OFPR_NO_MATCH = 0
    #: Action explicitly output to controller
    OFPR_ACTION = 1


# Classes


class PacketIn(GenericMessage):
    """Packet received on port (datapath -> controller)."""

    #: :class:`~pyof.v0x01.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_PACKET_IN)
    buffer_id = UBInt32()
    total_len = UBInt16()
    in_port = UBInt16()
    reason = UBInt8(enum_ref=PacketInReason)
    #: Align to 32-bits.
    pad = Pad(1)
    data = BinaryData()

    def __init__(self, xid=None, buffer_id=NO_BUFFER, total_len=None,
                 in_port=None, reason=None, data=b''):
        """Assign parameters to object attributes.

        Args:
            xid (int): Header's xid.
            buffer_id (int): ID assigned by datapath.
            total_len (int): Full length of frame.
            in_port (int): Port on which frame was received.
            reason (~pyof.v0x01.asynchronous.packet_in.PacketInReason):
                The reason why the packet is being sent
            data (bytes): Ethernet frame, halfway through 32-bit word, so the
                IP header is 32-bit aligned. The amount of data is inferred
                from the length field in the header. Because of padding,
                offsetof(struct ofp_packet_in, data) ==
                sizeof(struct ofp_packet_in) - 2.
        """
        super().__init__(xid)
        self.buffer_id = buffer_id
        self.total_len = total_len
        self.in_port = in_port
        self.reason = reason
        self.data = data
