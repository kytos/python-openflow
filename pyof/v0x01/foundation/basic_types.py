"""Defines basic types to be used in structures and messages."""

# System imports
import struct

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import exceptions

__all__ = ['UBInt8',
           'UBInt16',
           'UBInt32',
           'UBInt64',
           'Char']

# TODO: Refactor unpack methods to return the unpacked object
#       instead of being an inplace method.


class PAD(base.GenericType):
    """Class for padding attributes"""
    def __init__(self, size=0):
        self._size = size

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._size)

    def __str__(self):
        return str(self._size)

    def __set__(self, instance, value):
        # TODO: Check if value is of the same class
        raise exceptions.PADHasNoValue()

    def __delete__(self, instance):
        # TODO: This is the right delete way? Or should we delete
        #       the attribute from the instance?
        del self._size

    def __eq__(self, other):
        return self._size == other

    def __ne__(self, other):
        return self._size != other

    def __gt__(self, other):
        return self._size > other

    def __ge__(self, other):
        return self._size >= other

    def __lt__(self, other):
        return self._size <= other

    def __le__(self, other):
        return self._size <= other

    def get_size(self):
        """ Return the size of type in bytes. """
        return struct.calcsize("!{:d}B".format(self._size))

    def unpack(self, buff, offset):
        """Unpack a buff and stores at value property.
            :param buff:   Buffer where data is located.
            :param offset: Where data stream begins.
            Do nothing, since the _size is already defined
            and it is just a PAD. Keep buff and offset just
            for compability with other unpack methods
        """
        pass

    def pack(self):
        """Pack the object.

        Returns '\x00' multiplied by the size of the PAD
        """
        return '\x00' * self._size


class UBInt8(base.GenericType):
    """Format character for an Unsigned Char.

    Class for an 8 bits (1 byte) Unsigned Integer.
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
        """Unpack a buff and stores at value property.
            :param buff:   Buffer where data is located.
            :param offset: Where data stream begins.
        """
        self._value = struct.unpack_from(self._fmt, buff, offset)

    def pack(self):
        """Pack the object.

        Here we need a pointer, self.value is a tuple and is expanded to args.
        """
        return struct.pack(self._fmt, *self._value)


class UBInt16(base.GenericType):
    """Format character for an Unsigned Short.

    Class for an 16 bits (2 bytes) Unsigned Integer.
    """
    _fmt = "!H"


class UBInt32(base.GenericType):
    """Format character for an Unsigned Int.

    Class for an 32 bits (4 bytes) Unsigned Integer.
    """
    _fmt = "!I"


class UBInt64(base.GenericType):
    """Format character for an Unsigned Long Long.

    Class for an 64 bits (8 bytes) Unsigned Integer.
    """
    _fmt = "!Q"


class Char(base.GenericType):
    """Format double char to create a Char basic type."""
    def __init__(self, value=None, length=0):
        """Build a double char type according to the length
            :param value:  the character to be build.
            :param length: the character size.
        """
        if value:
            self._value = value
        self.length = length
        self._fmt = '!%d%c' % (self.length, 's')
