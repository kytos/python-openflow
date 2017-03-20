"""Defines buckets structures for controller2switch."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (FixedTypeList, Pad, UBInt16, UBInt32,
                                         UBInt64)
from pyof.v0x04.common.action import ActionHeader

__all__ = ('Bucket', 'BucketCounter',)


class Bucket(GenericStruct):
    """Bucket for use in groups."""

    length = UBInt16()
    weight = UBInt16()
    watch_port = UBInt32()
    watch_group = UBInt32()
    pad = Pad(4)
    actions = FixedTypeList(ActionHeader)

    def __init__(self, length=None, weight=None, watch_port=None,
                 watch_group=None, actions=None):
        """Initialize all instance variables.

        Args:
            length (int): Length the bucket in bytes, including this header and
                any padding to make it 64-bit aligned.
            weight (int): Relative weight of bucket. Only defined for select
                groups.
            watch_port (int): Port whose state affects whether this bucket is
                live. Only required for fast failover groups.
            watch_group (int): Group whose state affects whether this bucket is
                live. Only required for fast failover groups.
            actions (:func:`list` of :class:`.ActionHeader`): The action length
                is inferred from the length field in the header.
        """
        super().__init__()
        self.length = length
        self.weight = weight
        self.watch_port = watch_port
        self.watch_group = watch_group
        self.actions = actions


class BucketCounter(GenericStruct):
    """Used in group stats replies."""

    #: Number of packets processed by bucket.
    packet_count = UBInt64()
    #: Number of bytes processed by bucket.
    byte_count = UBInt64()

    def __init__(self, packet_count=None, byte_count=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            packet_count: Number of packets processed by bucket.
            byte_count: Number of bytes processed by bucket.
        """
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count


class ListOfActions(FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and used on ActionHeader objects.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (ActionHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=ActionHeader, items=items)
