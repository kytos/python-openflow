"""Switch replies to controller."""

# System imports

# Third-party imports

from pyof.v0x01.common import header as of_header
# Local source tree imports
from pyof.v0x01.common import phy_port, queue
from pyof.v0x01.foundation import base, basic_types

__all__ = ('QueueGetConfigReply',)


class QueueGetConfigReply(base.GenericMessage):
    """Class implements the response to the config request."""

    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REPLY)
    port = basic_types.UBInt16(enum_ref=phy_port.Port)
    #: Pad to 64-bits.
    pad = basic_types.PAD(6)
    queues = queue.ListOfQueues()

    def __init__(self, xid=None, port=None, queues=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid of OpenFlow header.
            port (Port): Target port for the query.
            queue (ListOfQueues): List of configured queues.
        """
        super().__init__(xid)
        self.port = port
        self.queues = [] if queues is None else queues
