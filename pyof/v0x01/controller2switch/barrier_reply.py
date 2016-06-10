"""Defines Barrier Reply message"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

# Classes


class BarrierReply(base.GenericMessage):
    """OpenFlow Barrier Reply Message.

    This message does not contain a body beyond the OpenFlow Header.

    :param xid: xid to be used on the message header
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_BARRIER_REPLY)

    def __init__(self, xid=None):
        super().__init__()
        self.header.xid = xid
