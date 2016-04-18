"""Defines basic types to be used in structures and messages."""

# System imports
import struct

# Third-party imports

# Local source tree imports
from ofp.v0x01.foudnation import base

__all__ = ['UBInt8',
           'UBInt8Array',
           'UBInt16',
           'UBInt32',
           'UBInt64',
           'Char']

# TODO: Refactor unpack methods to return the unpacked object
#       instead of being an inplace method.


class UBInt8(base.GenericType):
    """Format character for an Unsigned Char. Class for an 8 bytes
    Unsigned Integer.
    """
    _fmt = "!B"


class UBInt8Array(base.GenericType):
    """Creates an Array of Unsigned Integer of 8 bytes."""
    def __init__(self, value=None, length=0):
        if value:
            self._value = value
        self.length = length
        self._fmt = "!%d%c" % (self.length, 'B')

    def unpack(self, buff, offset=0):
        """ Unpack a buff and stores at value property.
            :param buff -- Buffer where data is located.
            :param offset -- Where data stream begins.
        """
        self._value = struct.unpack_from(self._fmt, buff, offset)

    def pack(self):
        """Pack the object.

        Here we need a pointer, self.value is a tuple and is expanded to args.
        """
        return struct.pack(self._fmt, *self._value)


class UBInt16(base.GenericType):
    """
    Format character for an Unsigned Short. Class for an 16 bytes
    Unsigned Integer.
    """
    _fmt = "!H"


class UBInt32(base.GenericType):
    """
    Format character for an Unsigned Int. Class for an 32 bytes
    Unsigned Integer.
    """
    _fmt = "!I"


class UBInt64(base.GenericType):
    """
    Format character for an Unsigned Long Long. Class for an 64 bytes
    Unsigned Integer.
    """
    _fmt = "!Q"


class Char(base.GenericType):
    """
    Format double char to create a Char basic type.
    """
    def __init__(self, value=None, length=0):
        """Build a double char type according to the length
            :param value: the character to be build.
            :param length: the character size.
        """
        if value:
            self._value = value
        self.length = length
        self._fmt = '!%d%c' % (self.length, 's')
