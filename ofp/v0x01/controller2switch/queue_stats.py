"""The OFPST_QUEUE stats reply message provides queue statistics for one
or more ports."""

# System imports

# Third-party imports

# Local source tree imports
from foundation import base
from foundation import basic_types


class QueueStats(base.GenericStruct):
    """
    Implements the reply body of a port_no

        :param port_no -- Port Number
        :param pad -- Align to 32-bits
        :param queue_id -- Queue ID
        :param tx_bytes -- Number of transmitted bytes
        :param tx_packets -- Number of transmitted packets
        :param tx_errors -- Number of packets dropped due to overrun
    """
    port_no = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=2)
    queue_id = basic_types.UBInt8()
    tx_bytes = basic_types.UBInt64()
    tx_packets = basic_types.UBInt64()
    tx_errors = basic_types.UBInt64()

    def __init__(self, port_no=None, pad=None, queue_id=None, tx_bytes=None,
                 tx_packets=None, tx_errors=None):

        self.port_no = port_no
        self.pad = pad
        self.queue_id = queue_id
        self.tx_bytes = tx_bytes
        self.tx_packets = tx_packets
        self.tx_errors = tx_errors
