"""Defines Barrier Reply message."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.v0x01.common.header import Header, Type

__all__ = ('BarrierReply',)

# Classes


class BarrierReply(GenericMessage):
    """OpenFlow Barrier Reply Message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_BARRIER_REPLY)
