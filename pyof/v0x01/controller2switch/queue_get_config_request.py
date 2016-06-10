"""Query the switch for configured queues on a port"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class QueueGetConfigRequest(base.GenericMessage):
    """Class implements the structure query for configured queues on a port.

    :param xid -- xid of OpenFlow header
    :param port -- Target port for the query
    :param pad -- Pad to 64-bits

    """
    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REQUEST)
    port = basic_types.UBInt16(enum_ref=phy_port.Port)
    pad = basic_types.PAD(2)

    def __init__(self, xid=None, port=None):
        super().__init__()
        self.header.xid = xid
        self.port = port
