from ofp.v0x02.types import UBInt8, UBInt16, UBInt32
from ofp.v0x02.consts import *

import collections

class Test(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [(key, type(value)) for key, value in 
                            classdict.items() if key not in 
                            ('__module__','__qualname__')]
        return type.__new__(self, name, bases, classdict)

class GenericStruct(metaclass=Test):
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
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                tot += (getattr(self, _attr).get_size())
            elif not callable(attr):
                tot += (_class(attr).get_size())
        return tot

    def build(self):
        hex = b''
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                hex += getattr(self, _attr).build()
                print("{} {} {}".format(_attr, attr,getattr(self, _attr).build()))
            elif not callable(attr):
                hex += _class(attr).build()
                print("{} {} {}".format(_attr, attr,_class(attr).build()))
        return hex

class GenericMessage(GenericStruct):
    def __init__(self, header, *args, **kwargs):
        """Receives the header and update the length field in it"""
        super().__init__(*args, **kwargs)
        self.header = header
        self.header.length = self.get_size()
        
    

class OFPHeader(GenericStruct):
    version = UBInt8()
    xid = UBInt32()
    length = UBInt16()
    ofp_type = UBInt8()

class OFPHello(GenericMessage):
    header = OFPHeader(version = 1 , xid = 10, ofp_type=0, length=2)
    x = UBInt32()

    def __init__(self, xid = 0, x = 0):
        header = OFPHeader(version = 1 , xid = xid, ofp_type=2, length=0)
        self.x = x
        super(OFPHello, self).__init__(header)



hello = OFPHello(xid=10,x=3)
print(hello.get_size())
print(hello.header.length)
print(hello.build())
