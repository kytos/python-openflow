"""Defines OpenFlow queues structures and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types

# Enums


class QueueProperties(enum.Enum):
    """
    Describes the queue properties.

    Enums:
        OFPQT_NONE      # No property defined for queue (default)
        OFPQT_MIN_RATE  # Minimum datarate guaranteed
    """
    OFPQT_NONE = 0
    OFPQT_MIN_RATE = 1


# Classes


class QueuePropHeader(base.GenericStruct):
    """
    This class describes the header of each queue property.

        :param property -- One of OFPQT_.
        :param len -- Length of property, including this header.
        :param pad -- 64-bit alignment.
    """
    property = basic_types.UBInt16()
    len = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=4)

    def __init__(self, property=None, len=None, pad=None):

        self.property = property
        self.len = len
        self.pad = pad


class PacketQueue(base.GenericStruct):
    """
    This class describes a queue.

        :param queue_id -- One of OFPQT_.
        :param length -- Length of property, including this header.
        :param pad --
        :param properties
    """
    queue_id = basic_types.UBInt32()
    length = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=2)
    properties = QueuePropHeader()

    def __init__(self, queue_id=None, length=None, pad=None, properties=None):

        self.queue_id = queue_id
        self.length = length
        self.pad = pad
        self.properties = properties


class QueuePropMinRate(base.GenericStruct):
    """
    This class defines the minimum-rate type queue.

        :param prop_reader -- prop: OFPQT_MIN, len: 16.
        :param rate -- In 1/10 of a percent; >1000 -> disabled.
        :param pad -- 64-bit alignmet.
    """
    prop_header = QueuePropHeader()
    rate = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=6)

    def __init__(self, prop_header=None, rate=None, pad=None):
        self.prop_header = prop_header
        self.rate = rate
        self.pad = pad
