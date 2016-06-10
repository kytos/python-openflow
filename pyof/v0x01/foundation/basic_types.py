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
    _fmt = ''

    def __init__(self, length=0):
        super().__init__()
        self._length = length

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._length)

    def __str__(self):
        return self.pack()

    def get_size(self):
        """ Return the size of type in bytes. """
        return struct.calcsize("!{:d}B".format(self._length))

    def unpack(self, buff, offset=0):
        """Unpack a buff and stores at value property.

        Do nothing, since the _length is already defined and it is just a PAD.
        Keep buff and offset just for compability with other unpack methods.

        :param buff:   Buffer where data is located.
        :param offset: Where data stream begins.
        """
        pass

    def pack(self):
        """Pack the object.

        Returns b'\x00' multiplied by the length of the PAD
        """
        return b'\x00' * self._length


class UBInt8(base.GenericType):
    """Format character for an Unsigned Char.

    Class for an 8 bits (1 byte) Unsigned Integer.
    """
    _fmt = "!B"


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
        super().__init__(value)
        self.length = length
        self._fmt = '!{}{}'.format(self.length, 's')

    def pack(self):
        packed = struct.pack(self._fmt, bytes(self.value, 'ascii'))
        return packed[:-1] + b'\0'  # null-terminated

    def unpack(self, buff, offset=0):
        try:
            begin = offset
            end = begin + self.length
            unpacked_data = struct.unpack(self._fmt, buff[begin:end])[0]
        except:
            raise Exception("%s: %s" % (offset, buff))

        self._value = unpacked_data.decode('ascii').rstrip('\0')


class HWAddress(base.GenericType):
    """Defines a hardware address"""

    def __init__(self, hw_address=b'000000'):
        super().__init__(hw_address)

    def pack(self):
        # struct.pack('!6B', *[int(x, 16) for x in self._value.split(':')])
        value = self._value.split(':')
        return struct.pack('!6B', *[int(x, 16) for x in value])

    def unpack(self, buff, offset=0):
        # value = ':'.join([hex(x)[2:] for x in struct.unpack('!6B', buff)])
        try:
            unpacked_data = struct.unpack('!6B', buff[offset:offset+6])
        except:
            raise Exception("%s: %s" % (offset, buff))
        transformed_data = ':'.join([hex(x)[2:] for x in unpacked_data])
        self._value = transformed_data

    def get_size(self):
        return 6


class BinaryData(base.GenericType):
    """Class to create objects that represents binary data

    This will be used on the 'data' attribute from
    packet_out and packet_in messages.

    Both the 'pack' and 'unpack' methods will return the binary data itself.
    get_size method will return the size of the instance using python 'len'
    """
    def __init__(self, value=b''):
        super().__init__(value)

    def pack(self):
        if isinstance(self._value, bytes):
            if len(self._value) > 0:
                return self._value
            else:
                return b''
        else:
            raise exceptions.NotBinaryData()

    def unpack(self, buff, offset=0):
        self._value = buff

    def get_size(self):
        return len(self._value)


class FixedTypeList(list, base.GenericStruct):
    """Creates a List that will receive OFP Classes"""
    _pyof_class = None

    def __init__(self, pyof_class, items=None):
        super().__init__()
        self._pyof_class = pyof_class
        if isinstance(items, list):
            self.extend(items)
        elif items:
            self.append(items)

    def __str__(self):
        """Human-readable object representantion"""
        return "{}".format([str(item) for item in self])

    def append(self, item):
        if isinstance(item, list):
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
        if len(self) == 0:
            return 0
        elif issubclass(self._pyof_class, base.GenericType):
            return len(self) * self._pyof_class().get_size()
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
        binary_items = [buff[i:i+item_size] for i in range(offset, len(buff),
                                                           item_size)]
        for binary_item in binary_items:
            item = self._pyof_class()
            item.unpack(binary_item)
            self.append(item)


class ConstantTypeList(list, base.GenericStruct):
    """Creates a List that will only allow objects of the same type (class) to
    be inserted"""
    def __init__(self, items=None):
        super().__init__()
        if isinstance(items, list):
            self.extend(items)
        elif items:
            self.append(items)

    def __str__(self):
        """Human-readable object representantion"""
        return "{}".format([str(item) for item in self])

    def append(self, item):
        if isinstance(item, list):
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
        if len(self) == 0:
            # If this is a empty list, then returns zero
            return 0
        elif issubclass(self[0].__class__, base.GenericType):
            # If the type of the elements is GenericType, then returns the
            # length of the list multiplied by the size of the GenericType.
            return len(self) * self[0].__class__().get_size()
        else:
            # Otherwise iter over the list accumulating the sizes.
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
