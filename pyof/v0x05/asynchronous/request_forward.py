"""Defines a Request Forward Message."""

# System imports

# Local source tree imports
from pyof.foundation.base import Enum, GenericStruct
from pyof.v0x05.common.header import Header, Type

# Third-party imports

__all__ = ('RequestForwardHeader', 'RequestForwardReason')


# Enums

class RequestForwardReason(Enum):
    """Request forward reason."""

    #: Forward group mod requests.
    OFPRFR_GROUP_MOD = 0
    #: Forward meter mod requests.
    OFPRFR_METER_MOD = 1


class RequestForwardHeader(GenericStruct):
    """Group/Meter request forwarding."""

    header = Header(Type.OFPT_REQUESTFORWARD)
    request = Header()

    def __init__(self, header=Header(Type.OFPT_REQUESTFORWARD),
                 request=Header):
        """Create an instance of the header.

            Args:
                header (Header): Type OFPT_REQUESTFORWARD.
                request (Header): Request being forwarded.
        """
        super().__init__()
        self.header = header
        self.request = request
