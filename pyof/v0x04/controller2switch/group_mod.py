"""Modify Group Entry Message."""
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import (
    FixedTypeList, Pad, UBInt8, UBInt16, UBInt32)
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.controller2switch.common import Bucket

__all__ = ('GroupMod', 'GroupModCommand', 'GroupType', 'Group')


class Group(IntEnum):
    """Group numbering. Groups can use any number up to OFPG_MAX."""

    #: Last usable group number.
    OFPG_MAX = 0xffffff00
    #: Fake groups.
    #: Represents all groups for group delete commands.
    OFPG_ALL = 0xfffffffc
    #: Wildcard group used only for flow stats requests.
    #  Select all flows regardless of group (including flows with no group).
    OFPG_ANY = 0xffffffff


class GroupModCommand(IntEnum):
    """Group commands."""

    #: New group.
    OFPGC_ADD = 0
    #: Modify all matching groups.
    OFPGC_MODIFY = 1
    #: Delete all matching groups.
    OFPGC_DELETE = 2


class GroupType(IntEnum):
    """Group types. Range [128, 255] is reserved for experimental use."""

    #: All (multicast/broadcast) group.
    OFPGT_ALL = 0
    #: Select group.
    OFPGT_SELECT = 1
    #: Indirect group.
    OFPGT_INDIRECT = 2
    #: Fast failover group.
    OFPGT_FF = 3


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
