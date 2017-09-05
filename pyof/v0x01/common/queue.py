"""Defines OpenFlow queues structures and related items."""

# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import FixedTypeList, Pad, UBInt16, UBInt32

# Third-party imports


__all__ = ('QueuePropHeader', 'PacketQueue', 'QueuePropMinRate',
           'QueueProperties', 'ListOfProperties', 'ListOfQueues')

# Enums


class QueueProperties(IntEnum):
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
        """Create a ListOfProperties with the optional parameters below.

        Args:
            items (:class:`list` of/or :class:`QueuePropHeader`):
                :class:`QueuePropHeader` instance or list of instances.
        """
        super().__init__(pyof_class=QueuePropHeader,
                         items=items)


class QueuePropHeader(GenericStruct):
    """Describe the header of each queue property."""

    queue_property = UBInt16(enum_ref=QueueProperties)
    length = UBInt16()
    #: 64-bit alignment
    pad = Pad(4)

    def __init__(self, queue_property=None, length=None):
        """Create a QueuePropHeader with the optional parameters below.

        Args:
            queue_property (~pyof.v0x01.common.queue.QueueProperties):
                The queue property.
            length (int): Length of property, including this header.
        """
        super().__init__()
        self.queue_property = queue_property
        self.length = length


class PacketQueue(GenericStruct):
    """Describe a queue."""

    queue_id = UBInt32()
    length = UBInt16()
    #: 64-bit alignment.
    pad = Pad(2)
    properties = ListOfProperties()

    def __init__(self, queue_id=None, length=None, properties=None):
        """Create a PacketQueue with the optional parameters below.

        Args:
            queue_id (int): ID of the specific queue.
            length (int): Length in bytes of this queue desc.
            properties(~pyof.v0x01.common.queue.ListOfProperties):
                Queue's list of properties. Default is an empty list.
        """
        super().__init__()
        self.queue_id = queue_id
        self.length = length
        self.properties = [] if properties is None else properties


class QueuePropMinRate(GenericStruct):
    """Define the minimum-rate type queue."""

    prop_header = QueuePropHeader(
        queue_property=QueueProperties.OFPQT_MIN_RATE, length=16)
    rate = UBInt16()
    #: 64-bit alignmet.
    pad = Pad(6)

    def __init__(self, rate=None):
        """Create a QueuePropMinRate with the optional parameters below.

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
        """Create a ListOfQueues with the optional parameters below.

        Args:
            items (:class:`list` of/or :class:`PacketQueue`):
                :class:`PacketQueue` instance or list of instances.
        """
        super().__init__(pyof_class=PacketQueue,
                         items=items)
