"""Switch replies to controller"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import queue
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class ListOfQueues(basic_types.FixedTypeList):
    """List of queues.

    Represented by instances of PacketQueue and
    used on QueueGetConfigReply objects

    Attributes:
        items (optional): Instance or a list of instances of PacketQueue
    """
    def __init__(self, items=[]):
        basic_types.FixedTypeList.__init__(self,
                                           pyof_class=queue.PacketQueue,
                                           items=items)


class QueueGetConfigReply(base.GenericMessage):
    """Class implements the response to the config request

        :param xid -- xid of OpenFlow header
        :param port -- Target port for the query
        :param pad -- Pad to 64-bits
        :param queue -- List of configured queues
    """
    header = of_header.Header()
    port = basic_types.UBInt16()
    pad = basic_types.PAD(6)
    queues = ListOfQueues()

    def __init__(self, xid=None, port=None, queues=[]):

        self.header.message_type = of_header.Type.OFPT_GET_CONFIG_REPLY
        self.header.xid = xid
        self.port = port
        self.queues = queues
