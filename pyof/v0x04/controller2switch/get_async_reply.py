"""Define GetAsyncReply message.

Response to the GetAsyncRequest message.
"""

# System imports

# Third-party imports

# Local imports
from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.common import AsyncConfig

__all__ = ('GetAsyncReply',)


class GetAsyncReply(AsyncConfig):
    """GetAsyncReply message.

    Response to GetAsyncRequest message.
    """

    def __init__(self, xid=None, packet_in_mask1=None, packet_in_mask2=None,
                 port_status_mask1=None, port_status_mask2=None,
                 flow_removed_mask1=None, flow_removed_mask2=None):
        """Set attributes for GetAsyncReply message.

        Args:
            xid (int): xid to be used on the message header.
            packet_in_mask1 (): .
            packet_in_mask2 (): .
            port_status_mask1 (): .
            port_status_mask2 (): .
            flow_removed_mask1 (): .
            flow_removed_mask2 (): .
        """
        super().__init__(xid, packet_in_mask1, packet_in_mask2,
                         port_status_mask1, port_status_mask2,
                         flow_removed_mask1, flow_removed_mask2)
        self.header.message_type = Type.OFPT_GET_ASYNC_REPLY
