"""Basic types used in structures and messages."""

# System imports
import struct

# Local source tree imports
from pyof.foundation import exceptions
from pyof.foundation.base import GenericStruct, GenericType

# Third-party imports

__all__ = ('BinaryData', 'Char', 'ConstantTypeList', 'FixedTypeList',
           'IPAddress', 'DPID', 'HWAddress', 'Pad', 'UBInt8', 'UBInt16',
           'UBInt32', 'UBInt64')


class Pad(GenericType):
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
        return '0' * self._length

    def get_size(self, value=None):
        """Return the type size in bytes.

        Args:
            value (int): In structs, the user can assign other value instead of
                this class' instance. Here, in such cases, ``self`` is a class
                attribute of the struct.

        Returns:
            int: Size in bytes.
        """
        return self._length

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        Do nothing, since the _length is already defined and it is just a Pad.
        Keep buff and offset just for compability with other unpack methods.

        Args:
            buff: Buffer where data is located.
            offset (int): Where data stream begins.
        """
        pass

    def pack(self, value=None):
        """Pack the object.

        Args:
            value (int): In structs, the user can assign other value instead of
                this class' instance. Here, in such cases, ``self`` is a class
                attribute of the struct.

        Returns:
            bytes: the byte 0 (zero) *length* times.
        """
        return b'\x00' * self._length


class UBInt8(GenericType):
    """Format character for an Unsigned Char.

    Class for an 8-bit (1-byte) Unsigned Integer.
    """

    _fmt = "!B"


class UBInt16(GenericType):
    """Format character for an Unsigned Short.

    Class for an 16-bit (2-byte) Unsigned Integer.
    """

    _fmt = "!H"


class UBInt32(GenericType):
    """Format character for an Unsigned Int.

    Class for an 32-bit (4-byte) Unsigned Integer.
    """

    _fmt = "!I"


class UBInt64(GenericType):
    """Format character for an Unsigned Long Long.

    Class for an 64-bit (8-byte) Unsigned Integer.
    """

    _fmt = "!Q"


class DPID(GenericType):
    """DataPath ID. Identifies a switch."""

    _fmt = "!8B"

    def __init__(self, dpid=None):
        """Create an instance and optionally set its dpid value.

        Args:
            dpid (str): E.g. 00:00:00:00:00:00:00:01.
        """
        super().__init__(value=dpid)

    def __str__(self):
        return self._value

    @property
    def value(self):
        """Return dpid value."""
        return self._value

    def pack(self, value=None):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()
        if value is None:
            value = self._value
        return struct.pack('!8B', *[int(v, 16) for v in value.split(':')])

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
        begin = offset
        hexas = []
        while begin < offset + 8:
            number = struct.unpack("!B", buff[begin:begin+1])[0]
            hexas.append("%.2x" % number)
            begin += 1
        self._value = ':'.join(hexas)


class Char(GenericType):
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

    def pack(self, value=None):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()

        try:
            if value is None:
                value = self.value
            packed = struct.pack(self._fmt, bytes(value, 'ascii'))
            return packed[:-1] + b'\0'  # null-terminated
        except struct.error as err:
            msg = "Char Pack error. "
            msg += "Class: {}, struct error: {} ".format(type(value).__name__,
                                                         err)
            raise exceptions.PackException(msg)

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


class IPAddress(GenericType):
    """Defines a IP address."""

    netmask = UBInt32()
    max_prefix = UBInt32(32)

    def __init__(self, address="0.0.0.0/32"):
        """The constructor takes the parameters below.

        Args:
            address (str): IP Address using ipv4.
                Defaults to '0.0.0.0/32'
        """
        if address.find('/') >= 0:
            address, netmask = address.split('/')
        else:
            netmask = 32

        super().__init__(address)
        self.netmask = int(netmask)

    def pack(self, value=None):
        """Pack the value as a binary representation.

        If the value is None the self._value will be used to pack.

        Args:
            value (str): IP Address with ipv4 format.

        Returns
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self._value

        if value.find('/') >= 0:
            value = value.split('/')[0]

        try:
            value = value.split('.')
            return struct.pack('!4B', *[int(x) for x in value])
        except struct.error as err:
            msg = "IPAddress error. "
            msg += "Class: {}, struct error: {} ".format(type(value).__name__,
                                                         err)
            raise exceptions.PackException(msg)

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
            unpacked_data = struct.unpack('!4B', buff[offset:offset+4])
            self._value = '.'.join([str(x) for x in unpacked_data])
        except struct.error as e:
            raise exceptions.UnpackException('%s; %s: %s' % (e, offset, buff))

    def get_size(self, value=None):
        """Return the ip address size in bytes.

        Args:
            value: In structs, the user can assign other value instead of
                this class' instance. Here, in such cases, ``self`` is a class
                attribute of the struct.

        Returns:
            int: The address size in bytes.
        """
        return 4


class HWAddress(GenericType):
    """Defines a hardware address."""

    def __init__(self, hw_address='00:00:00:00:00:00'):  # noqa
        """The constructor takes the parameters below.

        Args:
            hw_address (bytes): Hardware address. Defaults to
                '00:00:00:00:00:00'.
        """
        super().__init__(hw_address)

    def pack(self, value=None):
        """Pack the value as a binary representation.

        If the passed value (or the self._value) is zero (int), then the pack
        will assume that the value to be packed is '00:00:00:00:00:00'.

        Returns
            bytes: The binary representation.

        Raises:
            struct.error: If the value does not fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self._value

        if value == 0:
            value = '00:00:00:00:00:00'

        value = value.split(':')

        try:
            return struct.pack('!6B', *[int(x, 16) for x in value])
        except struct.error as err:
            msg = "HWAddress error. "
            msg += "Class: {}, struct error: {} ".format(type(value).__name__,
                                                         err)
            raise exceptions.PackException(msg)

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
        def _int2hex(n):
            return "{0:0{1}x}".format(n, 2)

        try:
            unpacked_data = struct.unpack('!6B', buff[offset:offset+6])
        except struct.error as e:
            raise exceptions.UnpackException('%s; %s: %s' % (e, offset, buff))

        transformed_data = ':'.join([_int2hex(x) for x in unpacked_data])
        self._value = transformed_data

    def get_size(self, value=None):
        """Return the address size in bytes.

        Args:
            value: In structs, the user can assign other value instead of
                this class' instance. Here, in such cases, ``self`` is a class
                attribute of the struct.

        Returns:
            int: The address size in bytes.
        """
        return 6

    def is_broadcast(self):
        """Return true if the value is a broadcast address. False otherwise."""
        return self.value == 'ff:ff:ff:ff:ff:ff'


class BinaryData(GenericType):
    """Class to create objects that represent binary data.

    This is used in the ``data`` attribute from
    :class:`~pyof.v0x01.asynchronous.packet_in.PacketIn` and
    :class:`~pyof.v0x01.controller2switch.packet_out.PacketOut` messages.
    Both the :meth:`pack` and :meth:`unpack` methods will return the
    binary data itself. :meth:`get_size` method will
    return the size of the instance using Python's :func:`len`.
    """

    def __init__(self, value=b''):  # noqa
        """The constructor takes the parameter below.

        Args:
            value (bytes): The binary data. Defaults to an empty value.

        Raises:
            ValueError: If given value is not bytes.
        """
        if not isinstance(value, bytes):
            raise ValueError('BinaryData must contain bytes.')
        super().__init__(value)

    def pack(self, value=None):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.

        Raises:
            :exc:`~.exceptions.NotBinaryData`: If value is not :class:`bytes`.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self._value

        if value:
            if isinstance(value, bytes):
                return value
            raise ValueError('BinaryData must contain bytes.')

        return b''

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. Since the *buff* is binary data, no conversion is done.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.
        """
        self._value = buff[offset:]

    def get_size(self, value=None):
        """Return the size in bytes.

        Args:
            value (bytes): In structs, the user can assign other value instead
                of this class' instance. Here, in such cases, ``self`` is a
                class attribute of the struct.

        Returns:
            int: The address size in bytes.
        """
        if value is None:
            return len(self._value)
        elif hasattr(value, 'get_size'):
            return value.get_size()

        return len(value)


class TypeList(list, GenericStruct):
    """Base class for lists that store objects of one single type."""

    def __init__(self, items):
        """Initialize the list with one item or a list of items.

        Args:
            items (iterable, ``pyof_class``): Items to be stored.
        """
        super().__init__()
        if isinstance(items, list):
            self.extend(items)
        elif items:
            self.append(items)

    def extend(self, items):
        """Extend the list by adding all items of ``items``.

        Args:
            items (iterable): Items to be added to the list.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has an unexpected
                type.
        """
        for item in items:
            self.append(item)

    def pack(self, value=None):
        """Pack the value as a binary representation.

        Returns:
            bytes: The binary representation.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self
        else:
            container = type(self)(items=None)
            container.extend(value)
            value = container

        bin_message = b''
        try:
            for item in value:
                bin_message += item.pack()
            return bin_message
        except exceptions.PackException as err:
            msg = "{} pack error: {}".format(type(self).__name__, err)
            raise exceptions.PackException(msg)

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
        begin = offset
        limit_buff = len(buff)

        while begin < limit_buff:
            item = item_class()
            item.unpack(buff, begin)
            self.append(item)
            begin += item.get_size()

    def get_size(self, value=None):
        """Return the size in bytes.

        Args:
            value: In structs, the user can assign other value instead of
                this class' instance. Here, in such cases, ``self`` is a class
                attribute of the struct.

        Returns:
            int: The size in bytes.
        """
        if value is None:
            if not self:
                # If this is a empty list, then returns zero
                return 0
            elif issubclass(type(self[0]), GenericType):
                # If the type of the elements is GenericType, then returns the
                # length of the list multiplied by the size of the GenericType.
                return len(self) * self[0].get_size()

            # Otherwise iter over the list accumulating the sizes.
            return sum(item.get_size() for item in self)

        return type(self)(value).get_size()

    def __str__(self):
        """Human-readable object representantion."""
        return "{}".format([str(item) for item in self])


class FixedTypeList(TypeList):
    """A list that stores instances of one pyof class."""

    _pyof_class = None

    def __init__(self, pyof_class, items=None):
        """The constructor parameters follows.

        Args:
            pyof_class (:obj:`type`): Class of the items to be stored.
            items (iterable, ``pyof_class``): Items to be stored.
        """
        self._pyof_class = pyof_class
        super().__init__(items)

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
        elif issubclass(item.__class__, self._pyof_class):
            list.append(self, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

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
        if issubclass(item.__class__, self._pyof_class):
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self._pyof_class.__name__)

    def unpack(self, buff, offset=0):
        """Unpack the elements of the list.

        This unpack method considers that all elements have the same size.
        To use this class with a pyof_class that accepts elements with
        different sizes, you must reimplement the unpack method.

        Args:
            buff (bytes): The binary data to be unpacked.
            offset (int): If we need to shift the beginning of the data.
        """
        super().unpack(buff, self._pyof_class, offset)


class ConstantTypeList(TypeList):
    """List that contains only objects of the same type (class).

    The types of all items are expected to be the same as the first item's.
    Otherwise, :exc:`~.exceptions.WrongListItemType` is raised in many
    list operations.
    """

    def __init__(self, items=None):  # noqa
        """The contructor can contain the items to be stored.

        Args:
            items (iterable, :class:`object`): Items to be stored.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
        super().__init__(items)

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
        elif not self:
            list.append(self, item)
        elif item.__class__ == self[0].__class__:
            list.append(self, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self[0].__class__.__name__)

    def insert(self, index, item):
        """Insert an item at the specified index.

        Args:
            index (int): Position to insert the item.
            item: Item to be inserted.

        Raises:
            :exc:`~.exceptions.WrongListItemType`: If an item has a different
                type than the first item to be stored.
        """
        if not self:
            list.append(self, item)
        elif item.__class__ == self[0].__class__:
            list.insert(self, index, item)
        else:
            raise exceptions.WrongListItemType(item.__class__.__name__,
                                               self[0].__class__.__name__)
