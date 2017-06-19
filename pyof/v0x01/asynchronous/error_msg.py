"""Defines an Error Message."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, UBInt16
from pyof.foundation.exceptions import PackException
# Do not import new_message_from_header directly to avoid cyclic import.
from pyof.v0x01.common.header import Header, Type

__all__ = ('ErrorMsg', 'ErrorType', 'BadActionCode', 'BadRequestCode',
           'FlowModFailedCode', 'HelloFailedCode', 'PortModFailedCode',
           'QueueOpFailedCode')


# Enums

class ErrorType(IntEnum):
    """Values for ’type’ in ofp_error_message.

    These values are immutable: they will not change in future versions of the
    protocol (although new values may be added).
    """

    #: Hello protocol failed
    OFPET_HELLO_FAILED = 0
    #: Request was not understood
    OFPET_BAD_REQUEST = 1
    #: Error in action description
    OFPET_BAD_ACTION = 2
    #: Problem in modifying Flow entry
    OFPET_FLOW_MOD_FAILED = 3
    #: Problem in modifying Port entry
    OFPET_PORT_MOD_FAILED = 4
    #: Problem in modifying Queue entry
    OFPET_QUEUE_OP_FAILED = 5

    def get_class(self):
        """Method used to return a Code class based on current ErrorType value.

        Returns:
            error_code_class (IntEnum): class referenced by current error type.
        """
        classes = {'OFPET_HELLO_FAILED': HelloFailedCode,
                   'OFPET_BAD_REQUEST': BadRequestCode,
                   'OFPET_BAD_ACTION': BadActionCode,
                   'OFPET_FLOW_MOD_FAILED': FlowModFailedCode,
                   'OFPET_PORT_MOD_FAILED': PortModFailedCode,
                   'OFPET_QUEUE_OP_FAILED': QueueOpFailedCode}
        return classes[self.name]


class HelloFailedCode(IntEnum):
    """Error_msg 'code' values for OFPET_HELLO_FAILED.

    'data' contains an ASCII text string that may give failure details.
    """

    #: No compatible version
    OFPHFC_INCOMPATIBLE = 0
    #: Permissions error
    OFPHFC_EPERM = 1


class BadRequestCode(IntEnum):
    """Error_msg 'code' values for OFPET_BAD_REQUEST.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: ofp_header.version not supported.
    OFPBRC_BAD_VERSION = 0
    #: ofp_header.type not supported.
    OFPBRC_BAD_TYPE = 1
    #: ofp_stats_request.type not supported.
    OFPBRC_BAD_STAT = 2
    #: Vendor not supported (in ofp_vendor_header or ofp_stats_request or
    #: ofp_stats_reply).
    OFPBRC_BAD_VENDOR = 3
    #: Vendor subtype not supported.
    OFPBRC_BAD_SUBTYPE = 4
    #: Permissions error.
    OFPBRC_EPERM = 5
    #: Wrong request length for type.
    OFPBRC_BAD_LEN = 6
    #: Specified buffer has already been used.
    OFPBRC_BUFFER_EMPTY = 7
    #: Specified buffer does not exist.
    OFPBRC_BUFFER_UNKNOWN = 8


class BadActionCode(IntEnum):
    """Error_msg 'code' values for OFPET_BAD_ACTION.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Unknown action type
    OFPBAC_BAD_TYPE = 0
    #: Length problem in actions
    OFPBAC_BAD_LEN = 1
    #: Unknown vendor id specified
    OFPBAC_BAD_VENDOR = 2
    #: Unknown action type for vendor id
    OFPBAC_BAD_VENDOR_TYPE = 3
    #: Problem validating output action
    OFPBAC_BAD_OUT_PORT = 4
    #: Bad action argument
    OFPBAC_BAD_ARGUMENT = 5
    #: Permissions error
    OFPBAC_EPERM = 6
    #: Can’t handle this many actions
    OFPBAC_TOO_MANY = 7
    #: Problem validating output queue
    OFPBAC_BAD_QUEUE = 8


class FlowModFailedCode(IntEnum):
    """Error_msg 'code' values for OFPET_FLOW_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Flow not added because of full tables
    OFPFMFC_ALL_TABLES_FULL = 0
    #: Attempted to add overlapping flow with CHECK_OVERLAP flag set
    OFPFMFC_OVERLAP = 1
    #: Permissions error
    OFPFMFC_EPERM = 2
    #: Flow not added because of non-zero idle/hard timeout
    OFPFMFC_BAD_EMERG_TIMEOUT = 3
    #: Unknown command
    OFPFMFC_BAD_COMMAND = 4
    #: Unsupported action list - cannot process in the order specified
    OFPFMFC_UNSUPPORTED = 5


class PortModFailedCode(IntEnum):
    """Error_msg 'code' values for OFPET_PORT_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Specified port does not exist
    OFPPMFC_BAD_PORT = 0
    #: Specified hardware address is wrong
    OFPPMFC_BAD_HW_ADDR = 1


class QueueOpFailedCode(IntEnum):
    """Error msg 'code' values for OFPET_QUEUE_OP_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Invalid port (or port does not exist)
    OFPQOFC_BAD_PORT = 0
    #: Queue does not exist
    OFPQOFC_BAD_QUEUE = 1
    #: Permissions error
    OFPQOFC_EPERM = 2


# Classes

class ErrorMsg(GenericMessage):
    """OpenFlow Error Message.

    This message does not contain a body in addition to the OpenFlow Header.
    """

    #: :class:`~pyof.v0x01.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_ERROR)
    error_type = UBInt16(enum_ref=ErrorType)
    code = UBInt16()
    data = BinaryData()

    def __init__(self, xid=None, error_type=None, code=None, data=b''):
        """Assign parameters to object attributes.

        Args:
            xid (int): To be included in the message header.
            error_type (:class:`ErrorType`): Error type.
            code (enum.IntEnum): Error code.
            data (bytes): Its content is based on the error type and code.
        """
        super().__init__(xid)
        self.error_type = error_type
        self.code = code
        self.data = data

    def pack(self, value=None):
        """Pack the value as a binary representation.

        :attr:`data` is packed before the calling :meth:`.GenericMessage.pack`.
        After that, :attr:`data`'s value is restored.

        Returns:
            bytes: The binary representation.
        """
        if value is None:
            data_backup = None
            if self.data is not None and not isinstance(self.data, bytes):
                data_backup = self.data
                self.data = self.data.pack()
            packed = super().pack()
            if data_backup is not None:
                self.data = data_backup
            return packed
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.
        """
        super().unpack(buff, offset)
        CodeClass = ErrorType(self.error_type).get_class()
        self.code = CodeClass(self.code)
