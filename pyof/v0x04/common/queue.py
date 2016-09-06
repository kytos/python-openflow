"""Defines OpenFlow queues structures and related items."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import FixedTypeList, Pad, UBInt16, UBInt32

# Third-party imports


__all__ = ('QueuePropHeader', 'PacketQueue', 'QueuePropMinRate',
           'QueueProperties', 'ListOfProperties', 'ListOfQueues')

# Enums


class QueueProperties(Enum):
    """Describe queue properties."""

    #: No property defined for queue (default)
    OFPQT_NONE = 0
    #: Minimum datarate guaranteed
    OFPQT_MIN_RATE = 1


# Classes


class ListOfProperties(FixedTypeList):
    """List of properties.

    Represented by instances of :class:`QueuePropHeader` and used on
    :class:`PacketQueue` objects.
    """

    def __init__(self, items=None):
        """The contructor takes the paremeters below.

        Args:
            items (:class:`list` of/or :class:`QueuePropHeader`):
                :class:`QueuePropHeader` instance or list of instances.
        """
        super().__init__(pyof_class=QueuePropHeader,
                         items=items)


class QueuePropHeader(GenericStruct):
    """Describe the header of each queue property."""

    property = UBInt16(enum_ref=QueueProperties)
    len = UBInt16()
    #: 64-bit alignment
    pad = Pad(4)

    def __init__(self, prop=None, length=None):
        """The contructor takes the paremeters below.

        Args:
            property (QueueProperties): The queue property.
            len (int): Length of property, including this header.
        """
        super().__init__()
        self.property = prop
        self.len = length


class PacketQueue(GenericStruct):
    """Describe a queue."""

    queue_id = UBInt32()
    length = UBInt16()
    #: 64-bit alignment.
    pad = Pad(2)
    properties = ListOfProperties()

    def __init__(self, queue_id=None, length=None, properties=None):
        """The contructor takes the paremeters below.

        Args:
            queue_id (int): ID of the specific queue.
            length (int): Length in bytes of this queue desc.
            properties(ListOfProperties): Queue's list of properties. Default
                is an empty list.
        """
        super().__init__()
        self.queue_id = queue_id
        self.length = length
        self.properties = [] if properties is None else properties


class QueuePropMinRate(GenericStruct):
    """Define the minimum-rate type queue."""

    prop_header = QueuePropHeader(prop=QueueProperties.OFPQT_MIN_RATE,
                                  length=16)
    rate = UBInt16()
    #: 64-bit alignmet.
    pad = Pad(6)

    def __init__(self, rate=None):
        """The contructor takes the paremeters below.

        Args:
            rate (int): In 1/10 of a percent (1000 -> 100%); >1000 -> disabled.
        """
        super().__init__()
        self.rate = rate


class ListOfQueues(FixedTypeList):
    """List of queues.

    Represented by instances of :class:`PacketQueue` and used on
    :class:`QueueGetConfigReply` objects.
    """

    def __init__(self, items=None):
        """The contructor takes the paremeters below.

        Args:
            items (:class:`list` of/or :class:`PacketQueue`):
                :class:`PacketQueue` instance or list of instances.
        """
        super().__init__(pyof_class=PacketQueue,
                         items=items)
