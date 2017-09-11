"""Defines Echo Reply message during the handshake."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData
from pyof.v0x01.common.header import Header, Type

__all__ = ('EchoReply',)

# Classes


class EchoReply(GenericMessage):
    """OpenFlow Reply message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_ECHO_REPLY, length=8)
    data = BinaryData()

    def __init__(self, xid=None, data=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
            data (bytes): arbitrary-length data field.
        """
        super().__init__(xid)
        self.data = BinaryData() if data is None else data
