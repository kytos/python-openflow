"""Defines Echo Reply message during the handshake."""

# System imports

# Third-party imports

from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.foundation.base import GenericMessage

__all__ = ('EchoReply',)

# Classes


class EchoReply(GenericMessage):
    """OpenFlow Reply message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_ECHO_REPLY,
                              length=8)

    def __init__(self, xid=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
