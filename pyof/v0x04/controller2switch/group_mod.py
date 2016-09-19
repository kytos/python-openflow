"""Modify Group Entry Message."""
from enum import Enum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import (FixedTypeList, GenericStruct, Pad,
                                         UBInt8, UBInt16, UBInt32)
from pyof.v0x04.common.action import ActionHeader
from pyof.v0x04.common.header import Header, Type

_all__ = ('GroupMod', 'GroupModCommand', 'GroupType', 'Bucket')


class GroupModCommand(Enum):
    """Group commands."""

    #: New group.
    OFPGC_ADD = 0
    #: Modify all matching groups.
    OFPGC_MODIFY = 1
    #: Delete all matching groups.
    OFPGC_DELETE = 2


class GroupType(Enum):
    """Group types. Range [128, 255] is reserved for experimental use."""

    #: All (multicast/broadcast) group.
    OFPGT_ALL = 0
    #: Select group.
    OFPGT_SELECT = 1
    #: Indirect group.
    OFPGT_INDIRECT = 2
    #: Fast failover group.
    OFPGT_FF = 3


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


class ListOfBuckets(FixedTypeList):
    """List of buckets.

    Represented by instances of Bucket.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (Bucket): Instance or a list of instances.
        """
        super().__init__(pyof_class=Bucket, items=items)


class GroupMod(GenericMessage):
    """Group setup and teardown (controller -> datapath)."""

    header = Header(message_type=Type.OFPT_GROUP_MOD)
    command = UBInt16(enum_ref=GroupModCommand)
    group_type = UBInt8()
    #: Pad to 64 bits.
    pad = Pad(1)
    group_id = UBInt32()
    buckets = ListOfBuckets()

    def __init__(self, xid=None, command=None, group_type=None, group_id=None,
                 buckets=None):
        """Initialize all instance variables.

        Args:
            xid (int): Header's transaction id. Defaults to random.
            command (GroupModCommand): One of OFPGC_*.
            group_type (GroupType): One of OFPGT_*.
            group_id (int): Group identifier.
            buckets (:class:`ListOfBuckets`): The length of the bucket
                array is inferred from the length field in the header.
        """
        super().__init__(xid)
        self.command = command
        self.group_type = group_type
        self.group_id = group_id
        self.buckets = buckets
