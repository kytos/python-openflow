"""
Contains basic and fundamental classes. Also few constants are defined here.
We designed python-openflow in a manner to make easy create new messages and
OpenFlow structs. You can realize that when you see a message class definition.

"""

# System imports
import collections
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
    def __init__(self):
        self._value = None

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._value)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, str(self._value))

    def __set__(self, instance, value):
        # TODO: Check if value is of the same class
        self._value = value

    def __delete__(self, instance):
        # TODO: This is the right delete way? Or should we delete
        #       the attribute from the instance?
        del self._value

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

    def validate(self):
        try:
            self.pack()
        except:
            raise


class MetaStruct(type):
    """
    MetaClass used to force ordered attributes
    """
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [(key, type(value))
                                    for key, value in
                                    classdict.items()
                                    if key[0] != '_' and not
                                    hasattr(value, '__call__')]
        return type.__new__(self, name, bases, classdict)


class GenericStruct(object):
    __metaclass__ = MetaStruct

    """Base class for all message classes (structs)"""
    def __init__(self, *args, **kwargs):
        for _attr, _class in self.__ordered__:
            if not callable(getattr(self, _attr)):
                # TODO: Validade data
                try:
                    setattr(self, _attr, kwargs[_attr])
                except KeyError:
                    pass

    def __repr__(self):
        message = self.__class__.__name__
        message += '('
        for _attr, _class in self.__ordered__:
            message += repr(getattr(self, _attr))
            message += ", "
        # Removing a comma and a space from the end of the string
        message = message[:-2]
        message += ')'
        return message

    def __str__(self):
        message = "{}:\n".format(self.__class__.__name__)
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if not hasattr(attr, '_fmt'):
                message += "  {}".format(str(attr).replace('\n','\n  '))
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
        tot = 0
        for _attr, _class in self.__ordered__:
            tot += getattr(self, _attr).get_size()
        return tot

    def pack(self):
        """Packs the message as binary.

        This method iters over the class attributes, according to the
        order of definition, and then converts each attribute to its byte
        representation using its own pack method.
            :return: binary representation of the message object
        """

        self.validate()
        message = b''
        for _attr, _class in self.__ordered__:
            message += getattr(self, _attr).pack()
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
        for _attr, _class in self.__ordered__:
            if _attr != "header":
                attribute = getattr(self, _attr)
                attribute.unpack(buff, offset=begin)
                begin += attribute.get_size()

    def _validate_attributes_type(self):
        """This method validates the type of each attribute"""
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if attr.__class__ is not _class:
                raise exceptions.AttributeTypeError(str(attr), attr.__class__,
                                                    self.__class__)
            if callable(getattr(attr, 'validate', None)):
                # If the attribute has a validate method, then call it too
                try:
                    attr.validate()
                except Exception as e:
                    message = str(e) + "\n"
                    message += self.__class__.__name__ + "." + _attr
                    if (_class.__name__):
                        message += "(" + repr(_class.__name__) + ")"
                    raise exceptions.BadValueException(message)

    def validate(self):
        """Method to validate the content of the object.

        Verifications:
            - attributes type
            - overflow behaviour
        """
        self._validate_attributes_type()


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
        self.validate()
        message = b''
        for _attr, _class in self.__ordered__:
            message += getattr(self, _attr).pack()
        return message
