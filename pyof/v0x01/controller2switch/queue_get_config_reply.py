"""Switch replies to controller."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt16
# Local source tree imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.common.queue import ListOfQueues

__all__ = ('QueueGetConfigReply',)


class QueueGetConfigReply(GenericMessage):
    """Class implements the response to the config request."""

    header = Header(message_type=Type.OFPT_QUEUE_GET_CONFIG_REPLY)
    port = UBInt16(enum_ref=Port)
    #: Pad to 64-bits.
    pad = Pad(6)
    queues = ListOfQueues()

    def __init__(self, xid=None, port=None, queues=None):
        """Create a QueueGetConfigReply with the optional parameters below.

        Args:
            xid (int): xid of OpenFlow header.
            port (~pyof.v0x01.common.phy_port.Port):
                Target port for the query.
            queue (~pyof.v0x01.common.queue.ListOfQueues):
                List of configured queues.
        """
        super().__init__(xid)
        self.port = port
        self.queues = [] if queues is None else queues
