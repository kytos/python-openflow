"""Defines Barrier Request message."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.v0x04.common.header import Header, Type

__all__ = ('BarrierRequest',)

# Classes


class BarrierRequest(GenericMessage):
    """OpenFlow Barrier Request Message.

    This message does not contain a body in addition to the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_BARRIER_REQUEST)
