"""Switch replies to controller"""

# System imports

# Third-party imports

# Local source tree imports
from common import header as of_header
from common import queue as of_queue
from foundation import base
from foundation import basic_types


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
    pad = basic_types.UBInt8Array(length=2)
    queue = of_queue.PacketQueue()
