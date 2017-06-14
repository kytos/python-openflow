"""Get Async Request Message."""
# System imports

# Third-party imports

# Local imports
from pyof.foundation.base import GenericMessage
from pyof.v0x04.common.header import Header, Type

__all__ = ('GetAsyncRequest',)


class GetAsyncRequest(GenericMessage):
    """Request Asynchronous messages.

    Query the asynchronous messages that it wants to receive (other than error
    messages) on a given OpenFlow channel.
    """

    #: OpenFlow :class:`~pyof.v0x04.common.header.Header`
    header = Header(message_type=Type.OFPT_GET_ASYNC_REQUEST)
