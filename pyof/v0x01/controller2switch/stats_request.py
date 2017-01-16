"""Query the datapath about its current state."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, UBInt16
# Local imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import (AggregateStatsRequest,
                                                 FlowStatsRequest,
                                                 PortStatsRequest,
                                                 QueueStatsRequest,
                                                 StatsTypes)

__all__ = ('StatsRequest',)


class StatsRequest(GenericMessage):
    """Request statistics to switch."""

    #: OpenFlow :class:`.Header`
    header = Header(message_type=Type.OFPT_STATS_REQUEST)
    body_type = UBInt16(enum_ref=StatsTypes)
    flags = UBInt16()
    body = BinaryData()

    _types = [None, FlowStatsRequest, AggregateStatsRequest,
              None, PortStatsRequest, QueueStatsRequest, None]

    def __init__(self, xid=None, body_type=None, flags=0, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            body_type (StatsTypes): One of the OFPST_* constants.
            flags (int): OFPSF_REQ_* flags (none yet defined).
            body (BinaryData): Body of the request.
        """
        super().__init__(xid)
        self.body_type = body_type
        self.flags = flags
        self.body = body

    def pack(self):
        """Pack according to :attr:`body_type`.

        Make `body` a binary pack before packing this object. Then, restore
        body.
        """
        if not self._types[self.body_type.value]:
            return super().pack()
        backup = self.body
        self.body = self.body.pack()
        pack = super().pack()
        self.body = backup
        return pack

    def unpack(self, buff):
        """Unpack according to :attr:`body_type`."""
        super().unpack(buff)
        buff = self.body.value
        self.body = self._types[self.body_type.value]()
        self.body.unpack(buff)
