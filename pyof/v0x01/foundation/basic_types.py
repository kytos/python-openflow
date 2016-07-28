"""Basic types used in structures and messages."""

# System imports
import struct

# Local source tree imports
from pyof.v0x01.foundation import base, exceptions

# Third-party imports


__all__ = ('UBInt8', 'UBInt16', 'UBInt32', 'UBInt64', 'Char', 'PAD',
           'HWAddress', 'BinaryData', 'FixedTypeList', 'ConstantTypeList')


class PAD(base.GenericType):
    """Class for padding attributes."""

    _fmt = ''

    def __init__(self, length=0):
        """Pad up to ``length``, in bytes.

        Args:
            length (int): Total length, in bytes.
        """
        super().__init__()
        self._length = length

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._length)

    def __str__(self):
        return self.pack()

    def get_size(self):
        """Return the type size in bytes.

        Returns:
            int: Size in bytes.
        """
        return struct.calcsize("!{:d}B".format(self._length))

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        Do nothing, since the _length is already defined and it is just a PAD.
        Keep buff and offset just for compability with other unpack methods.

        Args:
            buff: Buffer where data is located.
            offset (int): Where data stream begins.
        """
        pass

    def pack(self):
        """Pack the object.

        Return the byte 0 (zero) *length* times.

        Returns:
            bytes: A sequence of zeros.
        """
        return b'\x00' * self._length


class UBInt8(base.GenericType):
    """Format character for an Unsigned Char.

    Class for an 8-bit (1-byte) Unsigned Integer.
    """

    _fmt = "!B"


class UBInt16(base.GenericType):
    """Format character for an Unsigned Short.

    Class for an 16-bit (2-byte) Unsigned Integer.
    """

    _fmt = "!H"


class UBInt32(base.GenericType):
    """Format character for an Unsigned Int.

    Class for an 32-bit (4-byte) Unsigned Integer.
    """

    _fmt = "!I"


class UBInt64(base.GenericType):
    """Format character for an Unsigned Long Long.

    Class for an 64-bit (8-byte) Unsigned Integer.
    """

    _fmt = "!Q"


class Char(base.GenericType):
    """Build a double char type according to the length."""

    def __init__(self, value=None, length=0):
        """The constructor takes the optional parameters below.

        Args:
            value: The character to be build.
            length (int): Character size.
        """
        super().__init__(value)
        self.length = length
        self._fmt = '!{}{}'.format(self.length, 's')

    def pack(self):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        packed = struct.pack(self._fmt, bytes(self.value, 'ascii'))
        return packed[:-1] + b'\0'  # null-terminated

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            Exception: If there is a struct unpacking error.
        """
        try:
            begin = offset
            end = begin + self.length
            unpacked_data = struct.unpack(self._fmt, buff[begin:end])[0]
        except struct.error:
            raise Exception("%s: %s" % (offset, buff))

        self._value = unpacked_data.decode('ascii').rstrip('\0')


class HWAddress(base.GenericType):
    """Defines a hardware address."""

    def __init__(self, hw_address=b'000000'):
        """The constructor takes the parameters below.

        Args:
            hw_address (bytes): Hardware address. Defaults to b'000000'.
        """
        super().__init__(hw_address)

    def pack(self):
        """Pack the value as a binary representation.

        Returns
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        value = self._value.split(':')
        return struct.pack('!6B', *[int(x, 16) for x in value])

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            Exception: If there is a struct unpacking error.
        """
        try:
            unpacked_data = struct.unpack('!6B', buff[offset:offset+6])
        except:
            raise Exception("%s: %s" % (offset, buff))
        transformed_data = ':'.join([hex(x)[2:] for x in unpacked_data])
        self._value = transformed_data

    def get_size(self):
        """Return the address size in bytes.

        Returns:
            int: The address size in bytes.
        """
        return 6


class BinaryData(base.GenericType):
    """Class to create objects that represent binary data.

    This is used in the ``data`` attribute from :class:`.PacketIn` and
    :class:`.PacketOut` messages. Both the :meth:`pack` and :meth:`unpack`
    methods will return the binary data itself. :meth:`get_size` method will
    return the size of the instance using Python's :func:`len`.
    """

    def __init__(self, value=b''):
        """The constructor takes the parameter below.

        Args:
            value (bytes): The binary data. Defaults to an empty value.
        """
        super().__init__(value)

    def pack(self):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.

        Raises:
            :exc:`~.exceptions.NotBinaryData`: If value is not :class:`bytes`.
        """
        if isinstance(self._value, bytes):
            if len(self._value) > 0:
                return self._value
            else:
                return b''
        else:
            raise exceptions.NotBinaryData()

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. Since the *buff* is binary data, no conversion is done.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.
        """
        self._value = buff

    def get_size(self):
        """Return the size in bytes.

        Returns:
            int: The address size in bytes.
        """
        return len(self._value)


class FixedTypeList(list, base.GenericStruct):
    """A list that stores instances of one pyof class."""

    _pyof_class = None

    def __init__(self, pyof_class, items=None):
        """The constructor parameters follows.

        Args:
            pyof_class (:obj:`type`): Class of the items to be stored.
            items (iterable, ``pyof_class``): Items to be stored.
        """
        super().__init__()
        self._pyof_class = pyof_class
        if isinstance(items, list):
            self.extend(items)
        elif items:
            self.append(items)

    def __str__(self):
        """Human-readable object representation."""
        return "{}".format([str(item) for item in self])

    def append(self, item):
        """Append one item to the list.

        Args:
            item: Item to be appended. Its type must match the one defined in
                the constructor.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If the item has a different
                type than the one specified in the constructor.
        """
        if isinstance(item, list):
            self.extend(item)
        elif item.__class__ == self._pyof_class:
            list.append(self, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

    def extend(self, items):
        """Extend the list by adding all items of ``items``.

        Args:
            items (iterable): Must contain only items of the type defined in
                the constructor.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If any item has a different
                type than the one specified in the constructor.
        """
        for item in items:
            self.append(item)

    def insert(self, index, item):
        """Insert an item at the specified index.

        Args:
            index (int): Position to insert the item.
            item: Item to be inserted. It must have the type specified in the
                constructor.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If the item has a different
                type than the one specified in the constructor.
        """
        if item.__class__ == self._pyof_class:
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

    def get_size(self):
        """Return the size in bytes.

        Returns:
            int: The size in bytes.
        """
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
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.
        """
        bin_message = b''
        for item in self:
            bin_message += item.pack()
        return bin_message

    def unpack(self, buff, offset=0):
        """Unpack the elements of the list.

        This unpack method considers that all elements have the same size.
        To use this class with a pyof_class that accepts elements with
        different sizes, you must reimplement the unpack method.

        Args:
            buff (bytes): The binary data to be unpacked.
            offset (int): If we need to shift the beginning of the data.
        """
        item_size = self._pyof_class().get_size()
        binary_items = [buff[i:i+item_size] for i in range(offset, len(buff),
                                                           item_size)]
        for binary_item in binary_items:
            item = self._pyof_class()
            item.unpack(binary_item)
            self.append(item)


class ConstantTypeList(list, base.GenericStruct):
    """List that contains only objects of the same type (class).

    The types of all items are expected to be the same as the first item's.
    Otherwise, :exc:`~.exceptions.WrongListItemType` is raised in many
    list operations.
    """

    def __init__(self, items=None):
        """The contructor can contain the items to be stored.

        Args:
            items (iterable, :class:`object`): Items to be stored.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
        super().__init__()
        if isinstance(items, list):
            self.extend(items)
        elif items:
            self.append(items)

    def __str__(self):
        """Human-readable object representantion."""
        return "{}".format([str(item) for item in self])

    def append(self, item):
        """Append one item to the list.

        Args:
            item: Item to be appended.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
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
        """Extend the list by adding all items of ``items``.

        Args:
            items (iterable): Items to be added to the list.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
        for item in items:
            self.append(item)

    def insert(self, index, item):
        """Insert an item at the specified index.

        Args:
            index (int): Position to insert the item.
            item: Item to be inserted.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
        if len(self) == 0:
            list.append(self, item)
        elif item.__class__ == self[0].__class__:
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self[0].__class__.__name__)

    def get_size(self):
        """Return the size in bytes.

        Returns:
            int: The size in bytes.
        """
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
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.
        """
        bin_message = b''
        for item in self:
            bin_message += item.pack()
        return bin_message

    def unpack(self, buff, item_class, offset=0):
        """Unpack the elements of the list.

        This unpack method considers that all elements have the same size.
        To use this class with a pyof_class that accepts elements with
        different sizes, you must reimplement the unpack method.

        Args:
            buff (bytes): The binary data to be unpacked.
            item_class (:obj:`type`): Class of the expected items on this list.
            offset (int): If we need to shift the beginning of the data.
        """
        item_size = item_class.get_size()
        binary_items = [buff[i:i+2] for i in range(offset, len(buff),
                                                   item_size)]
        for binary_item in binary_items:
            item = item_class()
            item.unpack(binary_item)
            self.append(item)
