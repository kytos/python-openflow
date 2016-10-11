"""Response the stat request packet from the controller."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, UBInt16
# Local imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import FlowStats, StatsTypes

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

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``actions`` attribute which has a length determined
        by the ``actions_len`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
            offset (int): Where to begin unpacking.
        """
        stats = []
        super().unpack(buff, offset)
        data = self.body.value
        if self.body_type == StatsTypes.OFPST_FLOW:
            ReplyClass = FlowStats
        else:
            # TODO: Implement other types
            return

        while len(data) > 0:
            length = UBInt16()
            length.unpack(data[:2])
            item = ReplyClass()
            item.unpack(data[0:length.value])
            stats.append(item)
            data = data[length.value:]

        self.body = stats
