"""Query the switch for configured queues on a port"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class QueueGetConfigRequest(base.GenericStruct):
    """
    Class implements the structure query for configured queues on a port

        :param xid -- xid of OpenFlow header
        :param port -- Target port for the query
        :param pad -- Pad to 64-bits
    """
    header = of_header.Header()
    port = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=2)

    def __init__(self, xid=None, port=None, pad=None):

        self.header.message_type = of_header.Type.OFPT_GET_CONFIG_REQUEST
        self.header.xid = xid
        self.port = port
        self.pad = pad
