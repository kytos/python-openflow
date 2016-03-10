from ofp.v0x02.types import UBInt8

import collections

class Test(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [(key, type(value)) for key, value in classdict.items()
                                    if key not in
                                    ('__init__', '__module__','__qualname__')]
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
            else:
                tot += (_class(attr).get_size())
        return tot


    def build(self):
        hex = b''
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                hex += getattr(self, _attr).build()
            elif not callable(attr):
                hex += _class(attr).build()
        return hex.rstrip()

class GenericMessage(GenericStruct):
    pass

class OFPHeader(GenericMessage):
    type = UBInt8()
    version = UBInt8()
    xid = UBInt8()

class OFPHello(GenericMessage):
    header = OFPHeader(type = 2, version = 1 , xid = 10)
    x = UBInt8()


hello = OFPHello(x=3)
print(hello.build())
