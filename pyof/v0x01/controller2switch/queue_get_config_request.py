"""Query the switch for configured queues on a port."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt16
# Local source tree imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import Port

__all__ = ('QueueGetConfigRequest',)


class QueueGetConfigRequest(GenericMessage):
    """Query structure for configured queues on a port."""

    header = Header(message_type=Type.OFPT_QUEUE_GET_CONFIG_REQUEST)
    port = UBInt16(enum_ref=Port)
    #: Pad to 64-bits
    pad = Pad(2)

    def __init__(self, xid=None, port=None):
        """Create a QueueGetConfigRequest with the optional parameters below.

        Args:
            xid (int): xid of OpenFlow header
            port (~pyof.v0x01.common.phy_port.Port): Target port for the query
        """
        super().__init__(xid)
        self.port = port
