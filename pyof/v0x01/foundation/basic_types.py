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

        Returns b'\x00' multiplied by the size of the PAD
        """
        return b'\x00' * self._size


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


class FixedTypeList(list):
    """Creates a List that will receive OFP Classes"""
    _pyof_class = None

    def __init__(self, pyof_class, items=[]):
        self._pyof_class = pyof_class
        list.__init__(self, [])
        if items is not None and len(items) > 0:
            if type(items) is list:
                self.extend(items)
            else:
                self.append(items)

    def __repr__(self):
        """Unique representantion of the object.

        This can be used to generate an object that has the
        same content of the current object"""
        return "{}({},{})".format(self.__class__.__name__,
                                  self._pyof_class,
                                  self)

    def __str__(self):
        """Human-readable object representantion"""
        return "{}".format([item for item in self])

    def __set__(self, instance, value):
        """Clear the list and set value as the only item of the list"""
        self.__delete__(instance)
        self.append(value)

    def __delete__(self, instance):
        """This method remove all items from the list"""
        for item in self:
            self.remove(item)

    def append(self, item):
        if type(item) is list:
            self.extend(item)
        elif item.__class__ == self._pyof_class:
            list.append(self, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

    def extend(self, items):
        for item in items:
            self.append(item)

    def insert(self, index, item):
        if item.__class__ == self._pyof_class:
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

    def get_size(self):
        size = 0
        for item in self:
            size += item.get_size()
        return size

    def pack(self):
        bin_message = b''
        for item in self:
            bin_message += item.pack()
        return bin_message

    def unpack(self, buff, offset=0):
        """Unpacks the elements of the list

        This unpack method considers that all elements have the same size.
        To use this class with a pyof_class that accepts elements with
        different sizes you must reimplement the unpack method.

        Arguments:
            buff: the binary data to be unpacked
            offset: used if we need to shift the beginning of the data
        """
        item_size = self._pyof_class().get_size()
        binary_items = [buff[i:i+2] for i in range(offset, len(buff),
                                                   item_size)]
        for binary_item in binary_items:
            item = self._pyof_class()
            item.unpack(binary_item)
            self.append(item)


class ConstantTypeList(list):
    """Creates a List that will only allow objects of the same type (class) to
    be inserted"""
    def __init__(self, items=[]):
        list.__init__(self, [])
        if items is not None and len(items) > 0:
            if type(items) is list:
                self.extend(items)
            else:
                self.append(items)

    def __repr__(self):
        """Unique representantion of the object.

        This can be used to generate an object that has the
        same content of the current object"""
        return "{}({})".format(self.__class__.__name__,
                               self)

    def __str__(self):
        """Human-readable object representantion"""
        return "{}".format([item for item in self])

    def __set__(self, instance, value):
        """Clear the list and set value as the only item of the list"""
        self.__delete__(instance)
        self.append(value)

    def __delete__(self, instance):
        """This method remove all items from the list"""
        for item in self:
            self.remove(item)

    def append(self, item):
        if type(item) is list:
            self.extend(item)
        elif len(self) == 0:
            list.append(self, item)
        elif item.__class__ == self[0].__class__:
            list.append(self, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self[0].__class__.__name__)

    def extend(self, items):
        for item in items:
            self.append(item)

    def insert(self, index, item):
        if len(self) == 0:
            list.append(self, item)
        elif item.__class__ == self[0].__class__:
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self[0].__class__.__name__)

    def get_size(self):
        if getattr(self, 'len', None) and len(self) == 0:
            return 0
        else:
            size = 0
            for item in self:
                size += item.get_size()
            return size

    def pack(self):
        bin_message = b''
        for item in self:
            bin_message += item.pack()
        return bin_message

    def unpack(self, buff, item_class, offset=0):
        """Unpacks the elements of the list

        This unpack method considers that all elements have the same size.
        To use this class with a pyof_class that accepts elements with
        different sizes you must reimplement the unpack method.

        Arguments:
            buff: the binary data to be unpacked
            offset: used if we need to shift the beginning of the data
            item_class: Class of the expected items on this list
        """
        item_size = item_class.get_size()
        binary_items = [buff[i:i+2] for i in range(offset, len(buff),
                                                   item_size)]
        for binary_item in binary_items:
            item = item_class()
            item.unpack(binary_item)
            self.append(item)
