"""Defines an Error Message"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types
from pyof.v0x01.foundation import exceptions

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


class HelloFailedCode(enum.Enum):
    """Error_msg 'code' values for OFPET_HELLO_FAILED.
    'data' contains an ASCII text string that may give failure details.

        OFPHFC_INCOMPATIBLE  # No compatible version
        OFPHFC_EPERM         # Permissions error
    """
    OFPHFC_INCOMPATIBLE = 1,
    OFPHFC_EPERM = 2


class BadRequestCode(enum.Enum):
    """Error_msg 'code' values for OFPET_BAD_REQUEST.

    'data' contains at least the first 64 bytes of the failed request.
    """
    #: ofp_header.version not supported.
    OFPBRC_BAD_VERSION = 1
    #: ofp_header.type not supported.
    OFPBRC_BAD_TYPE = 2
    #: ofp_stats_request.type not supported.
    OFPBRC_BAD_STAT = 3
    #: Vendor not supported (in ofp_vendor_header or ofp_stats_request or
    #: ofp_stats_reply).
    OFPBRC_BAD_VENDOR = 4
    #: Vendor subtype not supported.
    OFPBRC_BAD_SUBTYPE = 5
    #: Permissions error.
    OFPBRC_EPERM = 6
    #: Wrong request length for type.
    OFPBRC_BAD_LEN = 7
    #: Specified buffer has already been used.
    OFPBRC_BUFFER_EMPTY = 8
    #: Specified buffer does not exist.
    OFPBRC_BUFFER_UNKNOWN = 9


class BadActionCode(enum.Enum):
    """Error_msg 'code' values for OFPET_BAD_ACTION.
    'data' contains at least the first 64 bytes of the failed request.

        OFPBAC_BAD_TYPE         # Unknown action type
        OFPBAC_BAD_LEN          # Length problem in actions
        OFPBAC_BAD_VENDOR       # Unknown vendor id specified
        OFPBAC_BAD_VENDOR_TYPE  # Unknown action type for vendor id
        OFPBAC_BAD_OUT_PORT     # Problem validating output action
        OFPBAC_BAD_ARGUMENT     # Bad action argument
        OFPBAC_EPERM            # Permissions error
        OFPBAC_TOO_MANY         # Can’t handle this many actions
        OFPBAC_BAD_QUEUE        # Problem validating output queue
    """
    OFPBAC_BAD_TYPE = 1,
    OFPBAC_BAD_LEN = 2,
    OFPBAC_BAD_VENDOR = 3,
    OFPBAC_BAD_VENDOR_TYPE = 4,
    OFPBAC_BAD_OUT_PORT = 5,
    OFPBAC_BAD_ARGUMENT = 6,
    OFPBAC_EPERM = 7,
    OFPBAC_TOO_MANY = 8,
    OFPBAC_BAD_QUEUE = 9


class FlowModFailedCode(enum.Enum):
    """Error_msg 'code' values for OFPET_FLOW_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """
    #: Flow not added because of full tables
    OFPFMFC_ALL_TABLES_FULL = 1
    #: Attempted to add overlapping flow with CHECK_OVERLAP flag set
    OFPFMFC_OVERLAP = 2
    #: Permissions error
    OFPFMFC_EPERM = 3
    #: Flow not added because of non-zero idle/hard timeout
    OFPFMFC_BAD_EMERG_TIMEOUT = 4
    #: Unknown command
    OFPFMFC_BAD_COMMAND = 5
    #: Unsupported action list - cannot process in the order specified
    OFPFMFC_UNSUPPORTED = 6


class PortModFailedCode(enum.Enum):
    """Error_msg 'code' values for OFPET_PORT_MOD_FAILED.
    'data' contains at least the first 64 bytes of the failed request.

        OFPPMFC_BAD_PORT     # Specified port does not exist
        OFPPMFC_BAD_HW_ADDR  # Specified hardware address is wrong
    """
    OFPPMFC_BAD_PORT = 1,
    OFPPMFC_BAD_HW_ADDR = 2


class QueueOpFailedCode(enum.Enum):
    """Error msg 'code' values for OFPET_QUEUE_OP_FAILED.
    'data' contains at least the first 64 bytes of the failed request.

        OFPQOFC_BAD_PORT   # Invalid port (or port does not exist)
        OFPQOFC_BAD_QUEUE  # Queue does not exist
        OFPQOFC_EPERM      # Permissions error
    """
    OFPQOFC_BAD_PORT = 1,
    OFPQOFC_BAD_QUEUE = 2,
    OFPQOFC_EPERM = 3


# Classes

class ErrorMsg(base.GenericMessage):
    """OpenFlow Error Message

    This message does not contain a body beyond the OpenFlow Header
        :param xid:    xid to be used on the message header
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_ERROR)
    error_type = basic_types.UBInt16(enum_ref=ErrorType)
    code = basic_types.UBInt16()
    data = basic_types.ConstantTypeList()

    def __init__(self, xid=None, error_type=None, code=None, data=None):
        super().__init__()
        self.header.xid = xid
        self.error_type = error_type
        self.code = code
        self.data = [] if data is None else data

    def unpack(self, buff, offset=0):
        # TODO: Implement the unpack method evaluation the error_type and code
        #       to unpack the data attribute
        raise exceptions.MethodNotImplemented("'Unpack' method not "
                                              "implemented on ErrorMsg class")
