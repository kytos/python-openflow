"""Query the switch for configured queues on a port."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt32
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import PortNo

__all__ = ('QueueGetConfigRequest',)


class QueueGetConfigRequest(GenericMessage):
    """Query structure for configured queues on a port."""

    #: Openflow :class:`~pyof.v0x04.common.header.Header`.
    header = Header(message_type=Type.OFPT_GET_CONFIG_REQUEST)
    #: Port to be queried. Should refer to a valid physical port
    #: (i.e. < OFPP_MAX), or OFPP_ANY to request all configured queues.
    port = UBInt32(enum_ref=PortNo)
    pad = Pad(4)

    def __init__(self, xid=None, port=None):
        """Create a QueueGetConfigRequest with the optional parameters below.

        Args:
            xid (int): xid of OpenFlow header
            port (:class:`~.common.port.PortNo`): Target port for the query.
        """
        super().__init__(xid)
        self.port = port
