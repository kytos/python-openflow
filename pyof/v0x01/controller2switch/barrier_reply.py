"""Defines Barrier Reply message."""

# System imports

# Third-party imports

from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

__all__ = ('BarrierReply')

# Classes


class BarrierReply(base.GenericMessage):
    """OpenFlow Barrier Reply Message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = of_header.Header(message_type=of_header.Type.OFPT_BARRIER_REPLY)

    def __init__(self, xid=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): Header's xid.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
