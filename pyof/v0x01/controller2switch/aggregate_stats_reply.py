"""Body of the reply message"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Classes


class AggregateStatsReply(base.GenericStruct):
    """
    Body of reply to OFPST_AGGREGATE request

        :param packet_count: Number of packets in flows
        :param byte_count:   Number of bytes in flows
        :param flow_count:   Number of flows
        :param pad:          Align to 64 bits
    """
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()
    flow_count = basic_types.UBInt32()
    pad = basic_types.PAD(4)

    def __init__(self, packet_count=None, byte_count=None, flow_count=None):

        self.packet_count = packet_count
        self.byte_count = byte_count
        self.flow_count = flow_count
