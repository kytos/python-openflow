"""Defines Barrier Request message."""

# System imports

# Third-party imports

from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

__all__ = ('BarrierRequest',)

# Classes


class BarrierRequest(base.GenericMessage):
    """OpenFlow Barrier Request Message.

    This message does not contain a body in addition to the OpenFlow Header.
    """

    header = of_header.Header(message_type=of_header.Type.OFPT_BARRIER_REQUEST)

    def __init__(self, xid=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
