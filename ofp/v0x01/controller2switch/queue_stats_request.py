"""The OFPST_QUEUE stats request message provides queue statistics for one
or more ports."""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class QueueStatsRequest(base.GenericStruct):
    """
    Implements the request body of a port_no

        :param port_no:  All ports if OFPT_ALL
        :param pad:      Align to 32-bits
        :param queue_id: All queues if OFPQ_ALL
    """
    port_no = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=2)
    queue_id = basic_types.UBInt32()

    def __init__(self, port_no=None, queue_id=None):

        self.port_no = port_no
        self.queue_id = queue_id
