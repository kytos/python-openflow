"""Query the switch for configured queues on a port."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

__all__ = ['QueueGetConfigRequest']


class QueueGetConfigRequest(base.GenericMessage):
    """Query structure for configured queues on a port.

    Args:
        xid (int): xid of OpenFlow header
        port (Port): Target port for the query
    """

    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REQUEST)
    port = basic_types.UBInt16(enum_ref=phy_port.Port)
    #: Pad to 64-bits
    pad = basic_types.PAD(2)

    def __init__(self, xid=None, port=None):
        super().__init__()
        self.header.xid = xid
        self.port = port
