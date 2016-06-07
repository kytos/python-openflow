# -*- coding: utf-8 -*-
"""
Contains basic and fundamental classes used in all library. Also few constants
are defined here. We designed python-openflow in a manner to make easy create
new messages and OpenFlow structs. You can realize that when you see a message
class definition.

A struct here is a group of basic attributes and/or struct attributes. For
instance, a :class:`~.common.header.Header` is a struct:

    >>> class Header(base.GenericStruct):
    >>>    version = basic_types.UBInt8()
    >>>    message_type = basic_types.UBInt8()
    >>>    length = basic_types.UBInt16()
    >>>    xid = basic_types.UBInt32()

A message here is like a struct but all messages has a header attribute. For
instance the :class:`~.asynchronous.packet_in.PacketIn` class is a message:

    >>> class PacketIn(base.GenericMessage):
    >>>     header = of_header.Header()
    >>>     buffer_id = basic_types.UBInt32()
    >>>     total_len = basic_types.UBInt16()
    >>>     in_port = basic_types.UBInt16()
    >>>     reason = basic_types.UBInt8()
    >>>     pad = basic_types.PAD(1)
    >>>     data = basic_types.BinaryData()

The main classes of this module are :class:`GenericStruct`,
:class:`GenericMessage`, :class:`GenericType` and :class:`MetaStruct`. Theses
classes are used in all part of this library.
"""

# System imports
from collections import OrderedDict as _OD
import enum
import struct
import copy

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import exceptions

# This will determine the order on sphinx documentation.
__all__ = ['GenericStruct', 'GenericMessage', 'GenericType', 'MetaStruct']

# Constants
OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_VERSION = 0x01
OFP_MAX_TABLE_NAME_LEN = 32
SERIAL_NUM_LEN = 32
DESC_STR_LEN = 256

# Classes


class GenericType(object):
    """This is a foundation class for all custom attributes.

    Attributes like `UBInt8`, `UBInt16`, `HWAddress` amoung others uses this
    class as base."""
    def __init__(self, value=None, enum_ref=None):
        self._value = value
        self._enum_ref = enum_ref

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)

    def __str__(self):
        return '{}'.format(str(self._value))

    def __eq__(self, other):
        return self._value == other

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

    def pack(self):
        """Pack the valeu as a binary representation."""
        if self.is_enum():
            if issubclass(type(self._value), GenericBitMask):
                value = self._value.bitmask
            else:
                # Gets the respective value from the Enum
                value = self._value.value
        else:
            value = self._value

        try:
            return struct.pack(self._fmt, value)
        except struct.error as err:
            message = "Value out of the possible range to basic type "
            message = message + type(self).__name__ + ". "
            message = message + str(err)
            raise exceptions.BadValueException(message)

    def unpack(self, buff, offset=0):
        """Unpack a buffer and stores at `_value` private attribute of a
        property.

        This method will convert a binary data into a readable value according
        to the attribute format.

        :param buff: binary buffer.
        :param offset: offset to be applied. Default is 0.
        """
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
            if self._enum_ref:
                self._value = self._enum_ref(self._value)
        except struct.error:
            raise exceptions.UnpackException("Error while unpacking"
                                             "data from buffer")

    def get_size(self):
        """Return the size in bytes of this attribute. """
        return struct.calcsize(self._fmt)

    def is_valid(self):
        """Check if an attribute is valid or not.

        This method will try to pack an attribute to the proper format.
        """
        # TODO Raise the proper exception here
        try:
            self.pack()
        except:
            raise

    def value(self):
        if isinstance(self._value, enum.Enum):
            return self._value.value
        else:
            return self._value

    def is_enum(self):
        return self._enum_ref is not None


class MetaStruct(type):
    """MetaClass used to force ordered attributes."""
    @classmethod
    def __prepare__(self, name, bases):
        return _OD()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = _OD([(key, type(value)) for
                                        key, value in classdict.items()
                                        if key[0] != '_' and not
                                        hasattr(value, '__call__')])
        return type.__new__(self, name, bases, classdict)


class GenericStruct(object, metaclass=MetaStruct):
    """Class that will be used by all OpenFlow structs.

    So, if you need insert a method that will be used for all Structs, here is
    the place to code.

    .. note:: A struct here on this library context is like a struct in C. It
              has a list of attributes and theses attributes can be of struct
              type too.
    """
    def __init__(self, *args, **kwargs):
        for _attr in self.__ordered__:
            if not callable(getattr(self, _attr)):
                try:
                    setattr(self, _attr, kwargs[_attr])
                except KeyError:
                    pass

    def _attributes(self):
        """Returns a generator with each attribute from the current instance.

        This attributes are coherced by the expected class for that attribute.
        """

        for _attr in self.__ordered__:
            _class = self.__ordered__[_attr]
            attr = getattr(self, _attr)
            if issubclass(_class, GenericType):
                # Checks for generic types
                if issubclass(type(attr), enum.Enum):
                    attr = _class(attr)
                elif not isinstance(attr, _class):
                    attr = _class(attr)
            elif issubclass(_class, list):
                # Verifications for classes derived from list type
                if not isinstance(attr, _class):
                    attr = _class(attr)
            yield (_attr, attr)

    def _attr_fits_into_class(attr, _class):
        if not isinstance(attr, _class):
            try:
                struct.pack(_class._fmt, attr)
            except:
                return False
        return True

    def _validate_attributes_type(self):
        """This method validates the type of each attribute"""
        for _attr in self.__ordered__:
            _class = self.__ordered__[_attr]
            attr = getattr(self, _attr)
            if isinstance(attr, _class):
                return True
            elif issubclass(_class, GenericType):
                if GenericStruct._fits_into_generic_type(attr, _class):
                    return True
            elif not isinstance(attr, _class):
                return False
        return True

    def get_class_attributes(self):
        for attr_name in self.__ordered__:
            yield (attr_name, getattr(type(self), attr_name))

    def get_instance_attributes(self):
        for attr_name in self.__ordered__:
            yield (attr_name, getattr(self, attr_name))

    def get_size(self):
        """Return the size (in bytes) of a struct.

        This method will call the `get_size()` method of each attribute or
        struct on the struct.

        So, if a struct has multiple attributes/structs this method will return
        the sum of each get_size of each attribute/struct.

        :returns: an `integer` that represents the number of bytes used by the
                  struct.
        """
        # TODO: raise the proper exception here
        if not GenericStruct.is_valid(self):
            raise Exception()
        else:
            size = 0
            for _attr, _class in self.__ordered__.items():
                attr = getattr(self, _attr)
                if _class.__name__ is 'PAD':
                    size += attr.get_size()
                elif _class.__name__ is 'Char':
                    size += getattr(type(self), _attr).get_size()
                elif issubclass(_class, GenericType):
                    size += _class().get_size()
                elif isinstance(attr, _class):
                    size += attr.get_size()
                else:
                    size += _class(attr).get_size()
            return size

    def pack(self):
        """Packs the struct as binary.

        This method iters over the class attributes, according to the
        order of definition, and then converts each attribute to its byte
        representation using its own pack method.

            :return: binary representation of the struct object.
        """
        if not self.is_valid():
            error_msg = "Erro on validation prior to pack() on class "
            error_msg += "{}.".format(type(self).__name__)
            raise exceptions.ValidationError(error_msg)
        else:
            message = b''
            for attr_name, attr_class in self.__ordered__.items():
                attr = getattr(self, attr_name)
                class_attr = getattr(type(self), attr_name)
                if isinstance(attr, attr_class):
                    message += attr.pack()
                elif class_attr.is_enum():
                    message += attr_class(value=attr,
                                          enum_ref=class_attr._enum_ref).pack()
                else:
                    message += attr_class(attr).pack()

            return message

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into the object attributes.

        This method updated the object attributes based on the unpacked data
        from a binary data. It is an inplace method, and it receives the binary
        data of the struct.

            :param buff: binary data package to be unpacked.
        """
        begin = offset
        for attribute_name, class_attribute in self.get_class_attributes():
            attribute = copy.deepcopy(class_attribute)
            attribute.unpack(buff, begin)
            setattr(self, attribute_name, attribute)
            begin += attribute.get_size()

    def is_valid(self):
        """Checks if all attributes on struct is valid.

        This method will check all attributes on struct if they have a proper
        value according to the OpenFlow specification.

        So for instance if you have a struct with any attribute of type
        :class:`basic_types.UBInt8()`, and you try to fill with a string
        value. This method will return false, because this struct is not valid.
        """
        # TODO: check for attribute types and overflow behaviour
        return True
        if not self._validate_attributes_type():
            return False
        return True


class GenericMessage(GenericStruct):
    """Base class that is the foundation for all OpenFlow messages.

    So, if you need insert a method that will be used for all messages, here is
    the place to code.

    .. note:: A Message on this library context is like a Struct but has a
              also a `header` attribute.
    """
    def unpack(self, buff, offset=0):
        """Unpack a binary message.

        This method updated the object attributes based on the unpacked
        data from the buffer binary message. It is an inplace method,
        and it receives the binary data of the message without the header.
        There is no return on this method

            :param buff: binary data package to be unpacked
                         without the first 8 bytes (header)
        """
        begin = offset
        for attribute_name, class_attribute in self.get_class_attributes():
            if type(class_attribute).__name__ != "Header":
                attribute = copy.deepcopy(class_attribute)
                attribute.unpack(buff, begin)
                setattr(self, attribute_name, attribute)
                begin += attribute.get_size()

    def _validate_message_length(self):
        if not self.header.length == self.get_size():
            return False
        return True

    def is_valid(self):
        """Check if a message is valid or not.

        This method will validate the content of the Message. You should call
        this method when you wanna verify if the message is ready to pack.

        During the validation process we check if the attribute values are
        valid according to OpenFlow specification.

        :returns: True or False.
        """
        return True
        if not super().is_valid:
            return False
        if not self._validate_message_length():
            return False
        return True

    def pack(self):
        """Packs the message into a binary data.

        One of the basic operations on a Message is the pack operation.

        During the packing process we get all attributes of a message and
        convert to binary.

        Since that this is usually used before send the message to switch, here
        we also call :func:`update_header_length`.

        :returns: A binary data thats represents the Message.
        """
        # TODO: Raise a proper lib exception
        self.update_header_length()
        if not self.is_valid():
            raise Exception("Error on validate")
        return super().pack()

    def update_header_length(self):
        """Updates the header length attribute based on message size.

        When sending an OpenFlow message we need to inform on header the length
        of the message. This is mandatory.

        This method update the packet header length with the actual message
        size.
        """
        self.header.length = self.get_size()


class MetaBitMask(type):
    """MetaClass used to create to create a special BitMaskEnum type.

    This metaclass converts the declared class attributes into elementes of an
    enum and stores it as _enum class attribute. It also replaces the __dir__
    and __getattr__ attributes, so the resulting Class will behave as an enum
    class (you can access object.ELEMENT and recover either values or names)
    """
    def __new__(self, name, bases, classdict):
        _enum = _OD([(key, value) for key, value in classdict.items()
                     if key[0] != '_' and not
                     hasattr(value, '__call__') and not
                     isinstance(value, property)])
        if len(_enum):
            classdict = {key: value for key, value in classdict.items()
                         if key[0] == '_' or hasattr(value, '__call__') or
                         isinstance(value, property)}
            classdict['_enum'] = _enum
        return type.__new__(self, name, bases, classdict)

    def __getattr__(cls, name):
        return cls._enum[name]

    def __dir__(cls):
        res = dir(type(cls)) + list(cls.__dict__.keys())
        if cls is not GenericBitMask:
            res.extend(cls._enum)
        return res


class GenericBitMask(object, metaclass=MetaBitMask):
    def __init__(self, bitmask=None):
        self.bitmask = bitmask

    def __str__(self):
        return "{}".format(self.bitmask)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.bitmask)

    @property
    def names(self):
        result = []
        for key, value in self._enum.items():
            if value & self.bitmask:
                result.append(key)
        return result
