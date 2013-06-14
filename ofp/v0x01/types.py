from struct import pack, unpack_from, calcsize

class GenericType():
    def __init__(self, value = None):
        if value:
           self.value = value

    def __str__(self):
        return str(self.value)

    def build(self):
        """ pack a value to a binnary buffer."""
        return pack(self.fmt, self.value)

    def parse(self, buff, offset=0):
        """ Unpack a buff and stores at value property. """
        self.value = unpack_from(self.fmt, buff, offset)[0]

    def get_size(self):
        """ Return the size of type in bytes. """
        return calcsize(self.fmt)


class UBInt8(GenericType):
    fmt = ">B"


class UBInt8Array(GenericType):
    def __init__(self, value = None, length = 0):
        if value:
            self.value = value
        self.length = length
        self.fmt = ">%d%c" % (self.length, 'B')

    def parse(self, buff, offset=0):
        self.value = unpack_from(self.fmt, buff, offset)

    def build(self):
        """
        Here we need a pointer, self.value is a tuple and is expanded to
        args.
        """
        return pack(self.fmt, *self.value)


class UBInt16(GenericType):
    fmt = ">H"


class UBInt32(GenericType):
    fmt = ">I"


class Char(GenericType):
    def __init__(self, value = None, length=0):
        if value:
            self.value = value
        self.length = length
        self.fmt = '>%d%c' % (self.length, 's')
