import collections


class GenericType():
    def __init__(self, value = 0):
       self.value = value

    def __str__(self):
        return str(self.value)

    def pack(self):
        """ Pack a value into a binary buffer."""
        return pack(self.fmt, self.value)

    def unpack(self, buff, offset=0):
        """ Unpack a buff and stores at value property. """
        try:
            self.value = unpack_from(self.fmt, buff, offset)[0]
        except error as e:
            raise OFPException("Error while unpack data from buffer")

    def get_size(self):
        """ Return the size of type in bytes. """
        return calcsize(self.fmt)


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
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                tot += (getattr(self, _attr).get_size())
            elif not callable(attr):
                tot += (_class(attr).get_size())
        return tot

    def pack(self):
        hex = b''
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                hex += getattr(self, _attr).pack()
                #print("{} {} {}".
                #      format(_attr, attr,getattr(self, _attr).pack()))
            elif not callable(attr):
                hex += _class(attr).pack()
                #print("{} {} {}"
                #      .format(_attr, attr,_class(attr).pack()))
        return hex

    def unpack(self, buff):
        begin = 0
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                size = (getattr(self, _attr).get_size())
                getattr(self,_attr).unpack(buff, offset=begin)
            elif not callable(attr):
                size = (_class(attr).get_size())
                getattr(self,_attr).unpack(buff, offset=begin)
            begin += size

