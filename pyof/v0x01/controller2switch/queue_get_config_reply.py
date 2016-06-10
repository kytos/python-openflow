"""Switch replies to controller"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.common import queue
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class QueueGetConfigReply(base.GenericMessage):
    """Class implements the response to the config request

    :param xid -- xid of OpenFlow header
    :param port -- Target port for the query
    :param pad -- Pad to 64-bits
    :param queue -- List of configured queues

    """
    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REPLY)
    port = basic_types.UBInt16(enum_ref=phy_port.Port)
    pad = basic_types.PAD(6)
    queues = queue.ListOfQueues()

    def __init__(self, xid=None, port=None, queues=None):
        super().__init__()
        self.header.xid = xid
        self.port = port
        self.queues = [] if queues is None else queues
