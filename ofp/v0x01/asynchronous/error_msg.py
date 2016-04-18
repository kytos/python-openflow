"""Defines an Error Message"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ..common import header as of_header
from ..foundation import base
from ..foundation import basic_types

# Enums

class ErrorType(enum.Enum):
    """
    Values for ’type’ in ofp_error_message.  These values are immutable: they
    will not change in future versions of the protocol (although new values
    may be added).

        OFPET_HELLO_FAILED      # Hello protocol failed
        OFPET_BAD_REQUEST       # Request was not understood
        OFPET_BAD_ACTION        # Error in action description
        OFPET_FLOW_MOD_FAILED   # Problem in modifying Flow entry
        OFPET_PORT_MOD_FAILED   # Problem in modifying Port entry
        OFPET_QUEUE_OP_FAILED   # # Problem in modifying Queue entry

    """
    OFPET_HELLO_FAILED = 1,
    OFPET_BAD_REQUEST = 2,
    OFPET_BAD_ACTION = 3,
    OFPET_FLOW_MOD_FAILED = 4,
    OFPET_PORT_MOD_FAILED = 5,
    OFPET_QUEUE_OP_FAILED = 6


class OFPError(base.GenericStruct):
    """OpenFlow Error Message

    This message does not contain a body beyond the OpenFlow Header
        :param length: length of the message
        :param xid: xid to be used on the message header
    """
    header = of_header.OFPHeader()
    type = basic_types.UBInt16()
    code = basic_types.UBInt16
    data = basic_types.UBInt8Array(length=0)

    def __init__(self, header=None, type=None, code=None, data=None):
        self.header.ofp_type = of_header.OFPType.OFPT_ERROR
        self.type =type
        self.code = code
        self.data = data
