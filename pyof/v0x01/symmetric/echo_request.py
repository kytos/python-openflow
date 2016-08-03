"""Defines Echo Request message during the handshake."""

# System imports

# Third-party imports

from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.foundation.base import GenericMessage

__all__ = ('EchoRequest',)

# Classes


class EchoRequest(GenericMessage):
    """OpenFlow Reply message.

    This message does not contain a body after the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_ECHO_REQUEST, length=8)

    def __init__(self, xid=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
