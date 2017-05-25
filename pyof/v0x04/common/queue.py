"""Defines OpenFlow queues structures and related items."""

# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, FixedTypeList, Pad, UBInt16, UBInt32)

# Third-party imports

__all__ = ('ListOfProperties', 'ListOfQueues', 'PacketQueue',
           'QueueProperties', 'QueuePropExperimenter', 'QueuePropHeader',
           'QueuePropMaxRate', 'QueuePropMinRate')

# Enums


class QueueProperties(IntEnum):
    """Describe queue properties."""

    #: Minimum datarate guaranteed
    OFPQT_MIN_RATE = 1
    #: Maximum datarate guaranteed
    OFPQT_MAX_RATE = 2
    #: Experimenter defined property
    OFPQT_EXPERIMENTER = 0xffff


# Classes


class QueuePropHeader(GenericStruct):
    """Describe the header of each queue property."""

    #: One of OFPQT_*
    queue_property = UBInt16(enum_ref=QueueProperties)
    #: Length of property, including this header
    length = UBInt16()
    #: 64-bit alignment
    pad = Pad(4)

    # pylint: disable=redefined-builtin
    def __init__(self, queue_property=None, length=None):
        """The contructor takes the paremeters below.

        Args:
            queue_property (~pyof.v0x04.common.queue.QueueProperties):
                The queue property.
            length (int): Length of property, including this header.
        """
        super().__init__()
        self.queue_property = queue_property
        self.length = length


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


class PacketQueue(GenericStruct):
    """Describe a queue."""

    #: id for the specific queue
    queue_id = UBInt32()
    #: Port this queue is attached to.
    port = UBInt32()
    #: Length, in bytes, of this queue desc.
    length = UBInt16()
    #: 64-bit alignment.
    pad = Pad(6)
    #: List of properties
    properties = ListOfProperties()

    def __init__(self, queue_id=None, port=None, length=None, properties=None):
        """The contructor takes the paremeters below.

        Args:
            queue_id (int): ID of the specific queue.
            port (int): Port his queue is attached to.
            length (int): Length in bytes of this queue desc.
            properties(~pyof.v0x04.common.queue.ListOfProperties):
                Queue's list of properties. Default is an empty list.
        """
        super().__init__()
        self.queue_id = queue_id
        self.port = port
        self.length = length
        self.properties = [] if properties is None else properties


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


class QueuePropExperimenter(GenericStruct):
    """Experimenter queue property uses the following structure and fields."""

    prop_header = QueuePropHeader(
        queue_property=QueueProperties.OFPQT_EXPERIMENTER, length=16)
    #: Experimenter ID which takes the same form as in struct
    #:     ofp_experimenter_header
    experimenter = UBInt32()
    #: 64-bit alignmet.
    pad = Pad(4)
    #: Experimenter defined data.
    data = BinaryData()

    def __init__(self, experimenter=None, data=None):
        """The contructor takes the paremeters below.

        Args:
            experimenter (int): Experimenter ID which takes the same form as in
                struct ofp_experimenter_header.
            data (bytes): Experimenter defined data.
        """
        super().__init__()
        self.experimenter = experimenter
        self.data = data


class QueuePropMaxRate(GenericStruct):
    """Maximum-rate queue property uses the following structure and fields."""

    prop_header = QueuePropHeader(
        queue_property=QueueProperties.OFPQT_MAX_RATE, length=16)
    #: In 1/10 of a percent; >1000 -> disabled.
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


class QueuePropMinRate(GenericStruct):
    """Minimum-rate queue property uses the following structure and fields."""

    prop_header = QueuePropHeader(
        queue_property=QueueProperties.OFPQT_MIN_RATE, length=16)
    #: In 1/10 of a percent; >1000 -> disabled.
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
