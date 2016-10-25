"""Response the stat request packet from the controller."""
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import (AggregateStatsReply,
                                                 DescStats, FlowStats,
                                                 PortStats, StatsTypes)

__all__ = ('StatsReply',)


class StatsReply(GenericMessage):
    """Class implements the response to the stats request."""

    #: OpenFlow :class:`.Header`
    header = Header(message_type=Type.OFPT_STATS_REPLY)
    body_type = UBInt16(enum_ref=StatsTypes)
    flags = UBInt16()
    body = BinaryData()

    def __init__(self, xid=None, body_type=None, flags=None, body=b''):
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

    def unpack(self, buff):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``body`` attribute which has its type determined
        by the ``body_type`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
        """
        super().unpack(buff)

        if self.body_type == StatsTypes.OFPST_PORT:
            self._unpack_body(FixedTypeList(pyof_class=PortStats))
        elif self.body_type == StatsTypes.OFPST_AGGREGATE:
            self._unpack_body(FixedTypeList(pyof_class=AggregateStatsReply))
        elif self.body_type == StatsTypes.OFPST_FLOW:
            self._unpack_body(FixedTypeList(pyof_class=FlowStats))
        elif self.body_type == StatsTypes.OFPST_DESC:
            self._unpack_body(DescStats())

    def _unpack_body(self, obj):
        """Unpack `body` using `obj` and replace it by the result."""
        obj.unpack(self.body.value)
        self.body = obj
