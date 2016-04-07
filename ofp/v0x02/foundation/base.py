"""Contains basic and fundamental classes and constants"""

# System imports
import collections
import struct

# Third-party imports

# Local source tree imports
from ofp.v0x02.foundation import exceptions


# CONSTANTS
OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_VERSION = 0x02

# CLASSES


class GenericType():
    def __init__(self, value = 0):
       self.value = value

    def __str__(self):
        return str(self.value)

    def pack(self):
        """ Pack a value into a binary buffer."""
        return struct.pack(self.fmt, self.value)

    def unpack(self, buff, offset=0):
        """ Unpack a buff and stores at value property. """
        try:
            self.value = struct.unpack_from(self.fmt, buff, offset)[0]
        except struct.error:
            raise exceptions.OFPException("Error while unpack data from buffer")

    def get_size(self):
        """ Return the size of type in bytes. """
        return struct.calcsize(self.fmt)


class MetaStruct(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [(key, type(value)) for key, value in
                            classdict.items() if key not in
                            ('__module__','__qualname__')]
        return type.__new__(self, name, bases, classdict)


class GenericStruct(metaclass=MetaStruct):
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
            tot += (attribute(self, _attr).get_size())
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
            hex += attribute(self, _attr).pack()
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
            begin += (attribute(self, _attr).get_size())
            getattr(self,_attr).unpack(buff, offset=begin)

    def attribute(self, _attr):
        attr = getattr(self, _attr)
        return _class(attr)
