"""Defines Barrier Reply message."""

# System imports

# Third-party imports

from pyof.v0x04.common.header import Header, Type
from pyof.foundation.base import GenericMessage

__all__ = ('BarrierReply',)

# Classes


class BarrierReply(GenericMessage):
    """OpenFlow Barrier Reply Message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_BARRIER_REPLY)

    def __init__(self, xid=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): Header's xid.
        """
        super().__init__(xid)