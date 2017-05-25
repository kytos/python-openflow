"""Switch replies to controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt32
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.common.queue import ListOfQueues

__all__ = ('QueueGetConfigReply',)


class QueueGetConfigReply(GenericMessage):
    """Class implements the response to the config request."""

    #: Openflow :class:`~pyof.v0x04.common.header.Header`.
    header = Header(message_type=Type.OFPT_GET_CONFIG_REPLY)
    #: Port to be queried. Should refer to a valid physical port
    #: (i.e. < OFPP_MAX), or OFPP_ANY to request all configured queues.
    port = UBInt32(enum_ref=PortNo)
    #: Pad to 64-bits.
    pad = Pad(4)
    #: List of configured queues.
    queues = ListOfQueues()

    def __init__(self, xid=None, port=None, queues=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid of OpenFlow header.
            port (:class:`~pyof.v0x04.common.port.PortNo`):
                Target port for the query.
            queue (:class:`~pyof.v0x04.common.queue.ListOfQueues`):
                List of configured queues.
        """
        super().__init__(xid)
        self.port = port
        self.queues = [] if queues is None else queues
