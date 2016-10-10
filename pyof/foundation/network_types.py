"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (BinaryData, FixedTypeList, HWAddress,
                                         UBInt8, UBInt16, UBInt64)

from pyof.foundation.exceptions import PackException

__all__ = ('Ethernet', 'GenericTLV', 'TLVWithSubType', 'LLDP')


class Ethernet(GenericStruct):
    destination = HWAddress()
    source = HWAddress()
    type = UBInt16()
    data = BinaryData()

    def __init__(self, destination=None, source=None, type=None, data=b''):
        super().__init__()
        self.destination = destination
        self.source = source
        self.type = type
        self.data = data

    def get_hash(self):
        return hash(self.pack())


class GenericTLV(GenericStruct):
    """TLV structure of LLDP packets.

    This is a Type, Length and Value struct.
    """
    def __init__(self, type=127, value=BinaryData()):
        self.type = type
        self.value = value

    @property
    def length(self):
        return len(self.value.pack())

    @property
    def header(self):
        return UBInt16(((self.type & 127) << 9) | (self.length & 511))

    def pack(self, value=None):
        """Pack the TLV in a binary representation.

        Returns:
            bytes: Binary representation of the struct object.

        Raises:
            :exc:`~.exceptions.ValidationError`: If validation fails.
        """
        if value is None:
            output = self.header.pack()
            output += self.value.pack()
            return output

        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buffer, offset=0):
        # TODO: Unpack is duplicated. We need to fix this.
        header = UBInt16()
        header.unpack(buffer[offset:offset+2])
        self.type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        self.value = BinaryData(buffer[begin:end])

    def get_size(self, value=None):
        # TODO: WTF ???!!?!?!?
        if isinstance(value, type(self)):
            return value.get_size()
        else:
            return 2 + self.length

class TLVWithSubType(GenericTLV):
    def __init__(self, type=1, sub_type=7, sub_value=BinaryData()):
        self.type = type
        self.sub_type = sub_type
        self.sub_value = BinaryData()

    @property
    def value(self):
        binary = UBInt8(self.sub_type).pack() + self.sub_value.pack()
        return BinaryData(binary)

    def unpack(self, buffer, offset=0):
        header = UBInt16()
        header.unpack(buffer[offset:offset+2])
        self.type = header.value >> 9
        length = header.value & 511 
        begin, end = offset + 2, offset + 2 + length
        sub_type = UBInt8()
        sub_type.unpack(buffer[begin:begin+1])
        self.sub_type = sub_type.value
        self.sub_value = BinaryData(buffer[begin+1:end])


class LLDP(GenericStruct):
    """LLDP class."""

    chassis_id = TLVWithSubType(type=1, sub_type=7)
    port_id = TLVWithSubType(type=2, sub_type=7)
    #: TTL time is given in seconds, between 0 and 65535
    ttl = GenericTLV(type=3, value=UBInt16(120))
    # We are not using list of tlvs for now
    #tlvs = ListOfTLVs()
    end = GenericTLV(type=0)
