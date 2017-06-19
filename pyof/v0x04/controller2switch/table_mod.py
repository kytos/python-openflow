"""Flow Table Modification message."""
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8, UBInt32
from pyof.v0x04.common.header import Header, Type

__all__ = ('Table', 'TableMod')


class Table(IntEnum):
    """Table numbering. Tables can use any number up to OFPT_MAX."""

    #: Last usable table number.
    OFPTT_MAX = 0xfe
    # Fake tables.
    #: Wildcard table used for table config, flow stats and flow deletes.
    OFPTT_ALL = 0xff


class TableMod(GenericMessage):
    """Configure/Modify behavior of a flow table."""

    header = Header(message_type=Type.OFPT_TABLE_MOD)
    table_id = UBInt8()
    #: Pad to 32 bits
    pad = Pad(3)
    config = UBInt32()

    def __init__(self, xid=None, table_id=None, config=None):
        """Assing parameters to object attributes.

        Args:
            xid (int): :class:`~pyof.v0x04.common.header.Header`'s xid.
                Defaults to random.
            table_id (int): ID of the table, OFPTT_ALL indicates all tables.
            config (int): Bitmap of OFPTC_* flags
        """
        super().__init__(xid)
        self.table_id = table_id
        self.config = config
