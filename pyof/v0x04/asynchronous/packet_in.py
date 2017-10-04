"""For packets received by the datapath and sent to the controller."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import (
    BinaryData, Pad, UBInt8, UBInt16, UBInt32, UBInt64)
from pyof.v0x04.common.flow_match import Match, OxmOfbMatchField
from pyof.v0x04.common.header import Header, Type

# Third-party imports


__all__ = ('PacketIn', 'PacketInReason')

# Enums


class PacketInReason(IntEnum):
    """Reason why this packet is being sent to the controller."""

    #: matching flow (table-miss flow entry).
    OFPR_NO_MATCH = 0
    #: Action explicitly output to controller.
    OFPR_ACTION = 1
    #: Packet has invalid TTL.
    OFPR_INVALID_TTL = 2


# Classes


class PacketIn(GenericMessage):
    """Packet received on port (datapath -> controller)."""

    #: :class:`~pyof.v0x04.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_PACKET_IN)
    #: ID assigned by datapath.
    buffer_id = UBInt32()
    #: Full length of frame.
    total_len = UBInt16()
    #: Reason packet is being sent (one of OFPR_*),
    reason = UBInt8(enum_ref=PacketInReason)
    #: ID of the table that was looked up.
    table_id = UBInt8()
    #: Cookie of the flow entry that was looked up.
    cookie = UBInt64()
    #: Packet metadata. Variable size.
    match = Match()
    #: Align to 64 bit + 16 bit
    pad = Pad(2)
    #: Ethernet frame whose length is inferred from header.length.
    #: The padding bytes preceding the Ethernet frame ensure that the IP
    #: header (if any) following the Ethernet header is 32-bit aligned.
    data = BinaryData()

    def __init__(self, xid=None, buffer_id=None, total_len=None, reason=None,
                 table_id=None, cookie=None, match=None, data=b''):
        """Assign parameters to object attributes.

        Args:
            xid (int): Header's xid.
            buffer_id (int): ID assigned by datapath.
            total_len (int): Full length of frame.
            reason (~pyof.v0x04.asynchronous.packet_in.PacketInReason):
                The reason why the packet is being sent
            table_id (int): ID of the table that was looked up
            cookie (int): Cookie of the flow entry that was looked up
            match (:class:`~pyof.v0x04.common.flow_match.Match`):
                Packet metadata with variable size.
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
        self.match = match
        self.data = data

    @property
    def in_port(self):
        """Retrieve the 'in_port' that generated the PacketIn.

        This method will look for the OXM_TLV with type OFPXMT_OFB_IN_PORT on
        the `oxm_match_fields` field from `match` field and return its value,
        if the OXM exists.

        Returns:
            The integer number of the 'in_port' that generated the PacketIn if
            it exists. Otherwise return None.

        """
        in_port = self.match.get_field(OxmOfbMatchField.OFPXMT_OFB_IN_PORT)
        return int.from_bytes(in_port, 'big')
