"""Switch replies to controller"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class QueueGetConfigReply(base.GenericStruct):
    """
    Class implements the response to the config request

        :param header -- OpenFlow header
        :param port -- Target port for the query
        :param pad -- Pad to 64-bits
        :param queue -- List of configured queues
    """
    header = of_header.OFPHeader()
    port = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=6)
    queue = of_queue.PacketQueue()

    def __init__(self, header=None, port=None, pad=None, queue=None):

        self.header = header
        self.port = port
        self.pad = pad
        self.queue = queue
