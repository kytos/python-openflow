"""Base and fundamental classes used all over the library.

Besides classes, several constants are defined here. We designed
python-openflow in a manner to make it easy to create new messages and OpenFlow
structs. You can realize that when you see a message class definition.

A **struct** here is a group of basic attributes and/or struct attributes (i.e.
:class:`~.common.header.Header`). A **message** here is like a struct, but all
messages have a header attribute (i.e.
:class:`~.asynchronous.packet_in.PacketIn`).

The main classes of this module are :class:`GenericStruct`,
:class:`GenericMessage`, :class:`GenericBitMask` and :class:`GenericType`.
These classes are used in all parts of this library.
"""

# System imports
import struct
from collections import OrderedDict
from copy import deepcopy
from enum import Enum

# Local source tree imports
from pyof.foundation.exceptions import (BadValueException, PackException,
                                        UnpackException, ValidationError)

# Third-party imports


# This will determine the order on sphinx documentation.
__all__ = ('GenericStruct', 'GenericMessage', 'GenericType', 'GenericBitMask',
           'MetaStruct', 'MetaBitMask')

# Classes


class GenericType:
    """Foundation class for all custom attributes.

    Base class for :class:`~.UBInt8`, :class:`~.Char`
    and others.
    """

    _fmt = None

    def __init__(self, value=None, enum_ref=None):
        """The constructor takes the optional parameters below.

        Args:
            value: The type's value.
            enum_ref (:class:`type`): If :attr:`value` is from an Enum, specify
                its type.
        """
        self._value = value
        self.enum_ref = enum_ref

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)

    def __str__(self):
        return '{}'.format(str(self._value))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pack() == other.pack()
        elif hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return self._value != other

    def __gt__(self, other):
        return self._value > other

    def __ge__(self, other):
        return self._value >= other

    def __lt__(self, other):
        return self._value <= other

    def __le__(self, other):
        return self._value <= other

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return self.value - other

    def __or__(self, other):
        return self.value | other

    def __ror__(self, other):
        return self.value | other

    def __and__(self, other):
        return self.value & other

    def __rand__(self, other):
        return self.value & other

    def __xor__(self, other):
        return self.value ^ other

    def __rxor__(self, other):
        return self.value ^ other

    @property
    def value(self):
        """Return this type's value.

        The value of an enum, bitmask, etc.
        """
        if self.isenum():
            if isinstance(self._value, self.enum_ref):
                return self._value.value
            return self._value
        elif self.is_bitmask():
            return self._value.bitmask
        else:
            return self._value

    def pack(self, value=None):
        r"""Pack the value as a binary representation.

        Considering an example with UBInt8 class, that inherits from
        GenericType:

        >>> from pyof.foundation.basic_types import UBInt8
        >>> objectA = UBInt8(1)
        >>> objectB = 5
        >>> objectA.pack()
        b'\x01'
        >>> objectA.pack(objectB)
        b'\x05'

        Args:
            value: If the value is None, then we will pack the value of the
                current instance. Otherwise, if value is an instance of the
                same type as the current instance, then we call the pack of the
                value object. Otherwise, we will use the current instance pack
                method on the passed value.

        Returns:
            bytes: The binary representation.

        Raises:
            :exc:`~.exceptions.BadValueException`: If the value does not
                fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self.value
        elif 'value' in dir(value):
            # if it is enum or bitmask gets only the 'int' value
            value = value.value

        try:
            return struct.pack(self._fmt, value)
        except struct.error:
            msg = '{} could not pack {} = {}.'.format(type(self).__name__,
                                                      type(value).__name__,
                                                      value)
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
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
            if self.enum_ref:
                self._value = self.enum_ref(self._value)
        except (struct.error, TypeError, ValueError) as e:
            msg = '{}; fmt = {}, buff = {}, offset = {}.'.format(e, self._fmt,
                                                                 buff, offset)
            raise UnpackException(msg)

    def get_size(self, value=None):
        """Return the size in bytes of this type.

        Returns:
            int: Size in bytes.
        """
        return struct.calcsize(self._fmt)

    def is_valid(self):
        """Check whether the value fits the binary format.

        Assert that :func:`pack` succeeds.

        Returns:
            bool: Whether the value is valid for this type.
        """
        try:
            self.pack()
            return True
        except BadValueException:
            return False

    def isenum(self):
        """Test whether it is an :class:`~Enum`.

        Returns:
            bool: Whether it is an :class:`~Enum`.
        """
        return self.enum_ref and issubclass(self.enum_ref, Enum)

    def is_bitmask(self):
        """Test whether it is a :class:`GenericBitMask`.

        Returns:
            bool: Whether it is a :class:`GenericBitMask`.
        """
        return self._value and issubclass(type(self._value), GenericBitMask)


class MetaStruct(type):
    """MetaClass to force ordered attributes.

    You probably do not need to use this class. Inherit from
    :class:`GenericStruct` instead.
    """

    @classmethod
    def __prepare__(mcs, name, bases):  # pylint: disable=unused-argument
        return OrderedDict()

    def __new__(mcs, name, bases, classdict):
        """Add ``__ordered__`` attribute with attributes in declared order."""
        # Skip methods and private attributes
        classdict['__ordered__'] = OrderedDict([(key, type(value)) for
                                                key, value in classdict.items()
                                                if key[0] != '_' and not
                                                hasattr(value, '__call__')])
        return type.__new__(mcs, name, bases, classdict)


class GenericStruct(object, metaclass=MetaStruct):
    """Class inherited by all OpenFlow structs.

    If you need to insert a method that will be used by all structs, this is
    the place to code it.

    .. note:: A struct on this library's context is like a struct in C. It
              has a list of attributes and theses attributes can be structs,
              too.
    """

    def __init__(self):
        """Contructor takes no argument and stores attributes' deep copies."""
        for name, value in self.get_class_attributes():
            setattr(self, name, deepcopy(value))

    def __eq__(self, other):
        """Check whether two structures have the same structure and values.

        Compare the binary representation of structs to decide whether they
        are equal or not.

        Args:
            other (GenericStruct): The struct to be compared with.
        """
        return self.pack() == other.pack()

    @staticmethod
    def _attr_fits_into_class(attr, cls):
        if not isinstance(attr, cls):
            try:
                struct.pack(cls._fmt, attr)  # pylint: disable=protected-access
            except struct.error:
                return False
        return True

    # linter cannot detect attribute added by metaclass
    # pylint: disable=no-member
    def _validate_attributes_type(self):
        """Validate the type of each attribute."""
        for _attr in self.__ordered__:
            _class = self.__ordered__[_attr]
            attr = getattr(self, _attr)
            if isinstance(attr, _class):
                return True
            elif issubclass(_class, GenericType):
                if GenericStruct._attr_fits_into_class(attr, _class):
                    return True
            elif not isinstance(attr, _class):
                return False
        return True

    def get_class_attributes(self):
        """Return a generator for class attributes' names and their types.

        .. code-block:: python3

            for _name, _type in self.get_class_attributes():
                print("Attribute name: {}".format(_name))
                print("Attribute type: {}".format(_type))

        Returns:
            generator: Tuples with attribute name and type.
        """
        for attribute_name in self.__ordered__:  # pylint: disable=no-member
            yield (attribute_name, getattr(type(self), attribute_name))

    def get_instance_attributes(self):
        """Return a generator for instance attributes' names and their values.

        .. code-block:: python3

            for _name, _value in self.get_instance_attributes():
                print("Attribute name: {}".format(_name))
                print("Attribute value: {}".format(_value))

        Returns:
            generator: Tuples with attribute name and value.
        """
        for attribute_name in self.__ordered__:  # pylint: disable=no-member
            yield (attribute_name, getattr(self, attribute_name))

    def get_attributes(self):
        """Return a generator for instance and class attribute.

        .. code-block:: python3

            for instance_attribute, class_attribute in self.get_attributes():
                print("Instance Attribute: {}".format(instance_attribute))
                print("Class Attribute: {}".format(class_attribute))

        Returns:
            generator: Tuples with instance attribute and class attribute
        """
        for attribute_name in self.__ordered__:  # pylint: disable=no-member
            yield (getattr(self, attribute_name),
                   getattr(type(self), attribute_name))

    def get_size(self, value=None):
        """Calculate the total struct size in bytes.

        For each struct attribute, sum the result of each one's ``get_size()``
        method.

        Args:
            value: In structs, the user can assign other value instead of a
                class' instance.

        Returns:
            int: Total number of bytes used by the struct.

        Raises:
            Exception: If the struct is not valid.
        """
        if value is None:
            # size = 0
            # for obj_val, cls_val in self.get_attributes():
            #     print('cls_val', cls_val, type(cls_val))
            #     print('obj_val', obj_val, type(obj_val))
            #     print('size is', cls_val.get_size(obj_val))
            #     size += cls_val.get_size(obj_val)
            # return size
            return sum(cls_val.get_size(obj_val) for obj_val, cls_val in
                       self.get_attributes())
        elif isinstance(value, type(self)):
            return value.get_size()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def pack(self, value=None):
        """Pack the struct in a binary representation.

        Iterate over the class attributes, according to the
        order of definition, and then convert each attribute to its byte
        representation using its own ``pack`` method.

        Returns:
            bytes: Binary representation of the struct object.

        Raises:
            :exc:`~.exceptions.ValidationError`: If validation fails.
        """
        if value is None:
            if not self.is_valid():
                error_msg = "Error on validation prior to pack() on class "
                error_msg += "{}.".format(type(self).__name__)
                raise ValidationError(error_msg)
            else:
                message = b''
                # pylint: disable=no-member
                for instance_attr, class_attr in self.get_attributes():
                    message += class_attr.pack(instance_attr)
                return message
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Update this object attributes based on the unpacked values of *buff*.
        It is an inplace method and it receives the binary data of the struct.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self.get_class_attributes():
            size = self._unpack_attribute(name, value, buff, begin)
            begin += size

    def _unpack_attribute(self, name, obj, buff, begin):
        attribute = deepcopy(obj)
        setattr(self, name, attribute)
        if len(buff) == 0:
            size = 0
        else:
            try:
                attribute.unpack(buff, begin)
                size = attribute.get_size()
            except UnpackException as e:
                child_cls = type(self).__name__
                msg = '{}.{}; {}'.format(child_cls, name, e)
                raise UnpackException(msg)
        return size

    def is_valid(self):
        """Check whether all struct attributes in are valid.

        This method will check whether all struct attributes have a proper
        value according to the OpenFlow specification. For instance, if you
        have a struct with an attribute of type :class:`UBInt8()`
        and you assign a string value to it, this method will return False.

        Returns:
            bool: Whether the struct is valid.
        """
        return True
        # pylint: disable=unreachable
        if not self._validate_attributes_type():
            return False
        return True


class GenericMessage(GenericStruct):
    """Base class that is the foundation for all OpenFlow messages.

    To add a method that will be used by all messages, write it here.

    .. note:: A Message on this library context is like a Struct but has a
              also a :attr:`header` attribute.
    """

    header = None

    def __init__(self, xid):
        """Initialize header's xid."""
        super().__init__()
        if xid is not None:
            self.header.xid = xid

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self.get_class_attributes():
            if type(value).__name__ != "Header":
                size = self._unpack_attribute(name, value, buff, begin)
                begin += size

    def _validate_message_length(self):
        if not self.header.length == self.get_size():
            return False
        return True

    def is_valid(self):
        """Check whether a message is valid or not.

        This method will validate the Message content. During the validation
        process, we check whether the attributes' values are valid according to
        the OpenFlow specification. Call this method if you want to verify
        whether the message is ready to pack.

        Returns:
            bool: Whether the message is valid.
        """
        return True
        # pylint: disable=unreachable
        if not super().is_valid():
            return False
        if not self._validate_message_length():
            return False
        return True

    def pack(self, value=None):
        """Pack the message into a binary data.

        One of the basic operations on a Message is the pack operation. During
        the packing process, we convert all message attributes to binary
        format.

        Since that this is usually used before sending the message to a switch,
        here we also call :meth:`update_header_length`.

        .. seealso:: This method call its parent's :meth:`GenericStruct.pack`
            after :meth:`update_header_length`.

        Returns:
            bytes: A binary data thats represents the Message.

        Raises:
            Exception: If there are validation errors.
        """
        if value is None:
            self.update_header_length()
            return super().pack()
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def update_header_length(self):
        """Update the header length attribute based on current message size.

        When sending an OpenFlow message we need to inform the message length
        on the header. This is mandatory.
        """
        self.header.length = self.get_size()


class MetaBitMask(type):
    """MetaClass to create a special BitMaskEnum type.

    You probably do not need to use this class. Inherit from
    :class:`GenericBitMask` instead.

    This metaclass converts the declared class attributes into elements of an
    enum. It also replaces the :meth:`__dir__` and :meth:`__getattr__` methods,
    so the resulting class will behave as an :class:`~Enum` class (you can
    access object.ELEMENT and recover either values or names).
    """

    def __new__(mcs, name, bases, classdict):
        """Convert class attributes into enum elements."""
        _enum = OrderedDict([(key, value) for key, value in classdict.items()
                             if key[0] != '_' and not
                             hasattr(value, '__call__') and not
                             isinstance(value, property)])
        if _enum:
            classdict = {key: value for key, value in classdict.items()
                         if key[0] == '_' or hasattr(value, '__call__') or
                         isinstance(value, property)}
            classdict['_enum'] = _enum
        return type.__new__(mcs, name, bases, classdict)

    def __getattr__(cls, name):
        return cls._enum[name]

    def __dir__(cls):
        res = dir(type(cls)) + list(cls.__dict__.keys())
        if cls is not GenericBitMask:
            res.extend(cls._enum)
        return res


class GenericBitMask(object, metaclass=MetaBitMask):
    """Base class for enums that use bitmask values."""

    def __init__(self, bitmask=None):
        """The constructor has the optional parameter below.

        Args:
            bitmask: Bitmask value.
        """
        self.bitmask = bitmask
        self._enum = {}

    def __str__(self):
        return "{}".format(self.bitmask)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.bitmask)

    @property
    def names(self):
        """List of selected enum names.

        Returns:
            list: Enum names.
        """
        result = []
        for key, value in self.iteritems():
            if value & self.bitmask:
                result.append(key)
        return result

    def iteritems(self):
        """Generator for attributes' name-value pairs.

        Returns:
            generator: Attributes' (name, value) tuples.
        """
        for key, value in self._enum.items():
            yield (key, value)
