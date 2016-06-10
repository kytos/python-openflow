"""Defines OpenFlow queues structures and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

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


class ListOfProperties(basic_types.FixedTypeList):
    """List of properties.

    Represented by instances of QueuePropHeader and
    used on PacketQueue objects

    :param items: (optional) Instance or a list of instances of QueuePropHeader
    """
    def __init__(self, items=None):
        super().__init__(pyof_class=QueuePropHeader,
                         items=items)


class QueuePropHeader(base.GenericStruct):
    """This class describes the header of each queue property.

        :param property: One of OFPQT\_.
        :param len:      Length of property, including this header.
        :param pad:      64-bit alignment.
    """
    property = basic_types.UBInt16(enum_ref=QueueProperties)
    len = basic_types.UBInt16()
    pad = basic_types.PAD(4)

    def __init__(self, property=None, len=None):
        super().__init__()
        self.property = property
        self.len = len


class PacketQueue(base.GenericStruct):
    """This class describes a queue.

    :param queue_id:   id for the specific queue
    :param length:     Length in bytes of this queue desc
    :param pad:        64-bit alignment
    :param properties: List of properties
    """
    queue_id = basic_types.UBInt32()
    length = basic_types.UBInt16()
    pad = basic_types.PAD(2)
    properties = ListOfProperties()

    def __init__(self, queue_id=None, length=None, properties=None):
        super().__init__()
        self.queue_id = queue_id
        self.length = length
        self.properties = [] if properties is None else properties


class QueuePropMinRate(base.GenericStruct):
    """This class defines the minimum-rate type queue.

    :param prop_header: prop: OFPQT_MIN_RATE, len: 16.
    :param rate:        In 1/10 of a percent; >1000 -> disabled.
    :param pad:         64-bit alignmet.
    """
    prop_header = QueuePropHeader(property=QueueProperties.OFPQT_MIN_RATE,
                                  len=16)
    rate = basic_types.UBInt16()
    pad = basic_types.PAD(6)

    def __init__(self, rate=None):
        super().__init__()
        self.rate = rate


class ListOfQueues(basic_types.FixedTypeList):
    """List of queues.

    Represented by instances of PacketQueue and
    used on QueueGetConfigReply objects

    :param items: (optional) Instance or a list of instances of PacketQueue
    """
    def __init__(self, items=None):
        super().__init__(pyof_class=PacketQueue,
                         items=items)
