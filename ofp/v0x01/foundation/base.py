"""Contains basic and fundamental classes and constants"""

# System imports
import collections
import struct

# Third-party imports

# Local source tree imports
from foundation import exceptions


# CONSTANTS
OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_VERSION = 0x02

# CLASSES


class GenericType(object):
    """This is a generic type Descriptor

    We can't implemment the __get__ method here
    """
    def __init__(self):
        self._value = None

    def __repr__(self):
        return str.format("{}({})", (self.__class__, self._value))

    def __str__(self):
        return str(self._value)

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
        """ Pack a value into a binary buffer."""
        return struct.pack(self._fmt, self._value)

    def unpack(self, buff, offset=0):
        """ Unpack a buff and stores at value property. """
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
        except struct.error:
            raise exceptions.OFPException("Error while unpack data from buffer")

    def get_size(self):
        """ Return the size of type in bytes. """
        return struct.calcsize(self._fmt)


class MetaStruct(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [(key, type(value)) for key, value in
                            classdict.items() if key[0] != '_']
        return type.__new__(self, name, bases, classdict)


class GenericStruct(object):
    __metaclass__ = MetaStruct
    def __init__(self, *args, **kwargs):
        for _attr, _class in self.__ordered__:
            if not callable(getattr(self, _attr)):
                # TODO: Validade data
                try:
                    setattr(self, _attr, kwargs[_attr])
                except KeyError:
                    pass

    def get_size(self):
        tot = 0
        for _attr, _class in self.__ordered__:
            #attr = getattr(self, _attr)
            #TODO: Ciclic reference
            # if _class is OFPHeader:
            #     tot += (getattr(self, _attr).get_size())
            # elif not callable(attr):
            #     tot += (_class(attr).get_size())
            #print(_attr)#, '-', getattr(self, _attr))
            tot += (self._field(_attr).get_size())
        return tot

    def pack(self):
        hex = b''
        for _attr, _class in self.__ordered__:
            #attr = getattr(self, _attr)
            #TODO: Ciclic reference
            # if _class is OFPHeader:
            #     hex += getattr(self, _attr).pack()
            #     #print("{} {} {}".
            #     #      format(_attr, attr,getattr(self, _attr).pack()))
            # elif not callable(attr):
            #     hex += _class(attr).pack()
            #     #print("{} {} {}"
            #     #      .format(_attr, attr,_class(attr).pack()))
            hex += _field(self, _attr).pack()
        return hex

    def unpack(self, buff):
        begin = 0
        for _attr, _class in self.__ordered__:
            #attr = getattr(self, _attr)
            #TODO: Ciclic reference
            # if _class is OFPHeader:
            #     size = (getattr(self, _attr).get_size())
            #     getattr(self,_attr).unpack(buff, offset=begin)
            # elif not callable(attr):
            #     size = (_class(attr).get_size())
            #     getattr(self,_attr).unpack(buff, offset=begin)
            # begin += size
            begin += (_field(self, _attr).get_size())
            getattr(self,_attr).unpack(buff, offset=begin)

    def _field(self, fieldName):
        attr = getattr(self, fieldName)
        return _class(attr)
