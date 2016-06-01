"""
Contains basic and fundamental classes. Also few constants are defined here.
We designed python-openflow in a manner to make easy create new messages and
OpenFlow structs. You can realize that when you see a message class definition.

"""

# System imports
from collections import OrderedDict
import enum
import struct

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import exceptions

#__all__ = ['OFP_ETH_ALEN', 'OFP_MAX_PORT_NAME_LEN', 'OFP_VERSION',
#           'OFP_MAX_TABLE_NAME_LEN', 'SERIAL_NUM_LEN', 'DESC_STR_LEN']

# CONSTANTS
OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_VERSION = 0x01
OFP_MAX_TABLE_NAME_LEN = 32
SERIAL_NUM_LEN = 32
DESC_STR_LEN = 256

# CLASSES


class GenericType(object):
    """This is a generic type Descriptor

    We can't implemment the __get__ method here
    """
    def __init__(self, val=None):
        self._value = val

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._value)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, str(self._value))

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
        if type(self._value.__class__) is enum.EnumMeta:
            # Gets the respective value from the Enum
            value = self._value.value
        else:
            value = self._value
        try:
            return struct.pack(self._fmt, value)
        except struct.error as err:
            message = "Value out of the possible range to basic type "
            message = message + self.__class__.__name__ + ". "
            message = message + str(err)
            raise exceptions.BadValueException(message)

    def unpack(self, buff, offset=0):
        """ Unpack a buff and stores at _value property. """
        # TODO: How to deal with this when the attribute from the
        #       owner class is an element from a enum? How to recover
        #       the enum name/reference ?
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
        except struct.error:
            raise exceptions.Exception("Error while unpacking"
                                       "data from buffer")

    def get_size(self):
        """ Return the size of type in bytes. """
        return struct.calcsize(self._fmt)

    def is_valid(self):
        try:
            self.pack()
        except:
            raise

    def value(self):
        return self._value


class MetaStruct(type):
    """
    MetaClass used to force ordered attributes
    """
    @classmethod
    def __prepare__(self, name, bases):
        return OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = OrderedDict([(key, type(value)) for
                                                key, value in classdict.items()
                                                if key[0] != '_' and not
                                                hasattr(value, '__call__')])
        return type.__new__(self, name, bases, classdict)


class GenericStruct(object):
    __metaclass__ = MetaStruct

    """Base class for all message classes (structs)"""
    def __init__(self, *args, **kwargs):
        for _attr in self.__ordered__:
            if not callable(getattr(self, _attr)):
                try:
                    setattr(self, _attr, kwargs[_attr])
                except KeyError:
                    pass

    def __repr__(self):
        message = self.__class__.__name__
        message += '('
        for _attr in self.__ordered__:
            message += repr(getattr(self, _attr))
            message += ", "
        # Removing a comma and a space from the end of the string
        message = message[:-2]
        message += ')'
        return message

    def __str__(self):
        message = "{}:\n".format(self.__class__.__name__)
        for _attr in self.__ordered__:
            attr = getattr(self, _attr)
            if not hasattr(attr, '_fmt'):
                message += "  {}".format(str(attr).replace('\n', '\n  '))
            else:
                message += "  {}: {}\n".format(_attr, str(attr))
        message.rstrip('\r')
        message.rstrip('\n')
        return message

    def get_size(self):
        """Return all tags whose names contain a given string.

        By default only free tags (tags which do not belong to any vocabulary)
        are returned. If the optional argument ``vocab_id_or_name`` is given
        then only tags from that vocabulary are returned.

        .. note:: test of a note

        :warning: test of a warning

        :class:`pyof.v0x01.common.header.Header` class.

        :param search_term: the string to search for in the tag names
        :type search_term: string
        :param vocab_id_or_name: the id or name of the vocabulary to look in
            (optional, default: None)
        :type vocab_id_or_name: string

        :returns: a list of tags that match the search term
        :rtype: list of ckan.model.tag.Tag objects

        These are written in doctest format, and should illustrate how to use
        the function.

                >>> a=[1,2,3]
                >>> print [x + 3 for x in a]
                [4, 5, 6]
        """
        if not GenericStruct.is_valid(self):
            raise Exception()
        else:
            size = 0
            for _attr in self.__ordered__:
                _class = self.__ordered__[_attr]
                attr = getattr(self, _attr)
                if _class.__name__ is 'PAD':
                    size += attr.get_size()
                elif _class.__name__ is 'Char':
                    size += getattr(self.__class__, _attr).get_size()
                elif issubclass(_class, GenericType):
                    size += _class().get_size()
                elif isinstance(attr, _class):
                    size += attr.get_size()
                else:
                    size += _class(attr).get_size()
            return size

    def _attributes(self):
        """Returns an generator with each attribute from the current instance.

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
            yield attr

    def pack(self):
        """Packs the message as binary.

        This method iters over the class attributes, according to the
        order of definition, and then converts each attribute to its byte
        representation using its own pack method.
            :return: binary representation of the message object
        """
        if not self.is_valid():
            error_msg = "Erro on validation prior to pack() on class "
            error_msg += "{}.".format(self.__class__.__name__)
            raise exceptions.ValidationError(error_msg)
        else:
            message = b''
            for attr in self._attributes():
                try:
                    message += attr.pack()
                except:
                    raise exceptions.AttributeTypeError(attr, type(attr),
                                                        type(attr))
            return message

    def unpack(self, buff):
        """Unpack a binary message.

        This method updated the object attributes based on the unpacked
        data from the buffer binary message. It is an inplace method,
        and it receives the binary data of the message without the header.
        There is no return on this method

            :param buff: binary data package to be unpacked
                         without the first 8 bytes (header)
        """
        begin = 0
        for attr in self._attributes:
            if attr.__class__.__name__ != "Header":
                attr.unpack(buff, offset=begin)
                setattr(self, attr.__name__, attr)
                begin += attr.get_size()

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

    def is_valid(self):
        """Method to validate the content of the object.

        Verifications:
            - attributes type
            - overflow behaviour
        """
        return True
        if not self._validate_attributes_type():
            return False
        return True


class GenericMessage(GenericStruct):
    """
    All OpenFlow messages here on this library will be based on this
    GenericMessage class.

    So, if you need insert a method that will be used for all messages, here is
    the place to code.
    """

    def update_header_length(self):
        """
        When sending an OpenFlow message we need to inform on header the length
        of the message. This is mandatory.

        This method update the packet header length with the actual message
        size.
        """
        self.header.length = self.get_size()

    def pack(self):
        """
        One of the basic operations on a Message is the pack operation.

        During the packing process we get all attributes of a message and
        convert to binary.

        Since that this is usually used before send the message to switch, here
        we also call :func:`update_header_length`. 
        """
        self.update_header_length()
        if not self.is_valid():
            raise Exception("Error on validate")
        return super().pack()

    def _validate_message_length(self):
        if not self.header.length == self.get_size():
            return False
        return True

    def is_valid(self):
        return True
        if not super().is_valid:
            return False
        if not self._validate_message_length():
            return False
        return True
