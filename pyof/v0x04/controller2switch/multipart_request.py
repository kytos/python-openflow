"""Controller requesting state from datapath."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, Pad, UBInt16
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.controller2switch.common import MultipartTypes

# Third-party imports


__all__ = ('MultipartRequest', 'MultipartRequestFlags')

# Enum


class MultipartRequestFlags(Enum):
    """Flags for MultipartRequest."""

    #: More requests to follow
    OFPMPF_REQ_MORE = 1 << 0


# Classes


class MultipartRequest(GenericMessage):
    """Request datapath state.

    While the system is running, the controller may request state from the
    datapath using the OFPT_MULTIPART_REQUEST message.
    """

    #: :class:`~.common.header.Header`
    header = Header(message_type=Type.OFPT_PORT_MOD)
    #: One of the OFPMP_* constants.
    multipart_type = UBInt16(enum_ref=MultipartTypes)
    #: OFPMPF_REQ_* flags.
    flags = UBInt16(enum_ref=MultipartRequestFlags)
    #: Padding
    pad = Pad(4)
    #: Body of the request
    body = BinaryData()

    def __init__(self, xid=None, multipart_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to the header.
            multipart_type (int): One of the OFPMP_* constants.
            flags (int): OFPMPF_REQ_* flags.
            body (bytes): Body of the request.
        """
        super().__init__(xid)
        self.multipart_type = multipart_type
        self.flags = flags
        self.body = body
