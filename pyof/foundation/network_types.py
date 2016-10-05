"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (BinaryData, FixedTypeList, HWAddress,
                                         UBInt8, UBInt16, UBInt64)

__all__ = ('Ethernet', 'LLDP', 'LLDP_TLV')
from pyof.foundation.exceptions import PackException


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

    def __hash__(self):
        return hash(self.pack())

    def get_hash(self):
        return self.__hash__()


class LLDP_TLV(GenericStruct):
    """TLV structure of LLDP packets."""

    #: This field actually have 7 bits, so on pack/unpack we will need to do
    #: some magic.
    type = UBInt8()
    #: Defines the length of subtype + value This field actually have 9 bits.
    length = UBInt8()
    #: Binary data to be passed along. No matter the type and length, here you
    #: will always need to add content as binary data. So, if you have
    #: something that is not binary (bytes), then pack it befor adding.
    value = BinaryData()

    def __init__(self, type, value=None):
        self.type = type
        self.value = value if value is not None else b''

    def _type_is_valid(self):
        """Check if the type value can be represented in 7 bits."""
        # 7 bits can represent 128 values, from 0 to 127.
        if self.type >= 0 and self.type < 128:
            return True
        else:
            return False

    def _length_is_valid(self):
        """Check if the length value can be represented in 9 bits."""
        # 9 bits can represent 512 values, from 0 to 511
        if self.length >= 0 and self.length < 511:
            return True
        else:
            return False

    def update_length(self):
        """Updates the length attribute of the instance."""
        self.length = len(BinaryData().pack(self.value))

    def pack(self, value=None):
        """Pack the LLDP_TLV in a binary representation.

        Returns:
            bytes: Binary representation of the struct object.

        Raises:
            :exc:`~.exceptions.ValidationError`: If validation fails.
        """
        if value is None:
            output = b''

            # Packing the 7bits type field
            if not self._type_is_valid():
                error_msg = '%s is not a valid value for TLV_type field'
                raise PackException(error_msg, self.type)

            self.update_length()

            if not self._length_is_valid():
                error_msg = '%s is not a valid value for TLV_length field'
                raise PackException(error_msg, self.length)

            # Here we are gathering the 7 bits from self.type with the higher
            # bit from self.length to pack it in one byte.
            output += UBInt8().pack(self.type << 1 | self.length >> 8)
            # Here we are removing the higher bit from length to pack it as
            # 1 byte also.
            output += UBInt8().pack(self.length & ((1 << 8) - 1))
            output += BinaryData().pack(self.value)

            return output
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buffer, offset=0):
        buffer = buffer[offset:]
        type_and_length = UBInt16().unpack(buffer[0:16]).value
        self.type = type_and_length >> 9
        self.length = type_and_length & ((1 << 10) - 1)
        self.value = BinaryData().unpack(buffer[16:16+self.length])

    def get_size(self, value=None):
        if isinstance(value, type(self)):
            return value.get_size()
        else:
            return 2 + len(BinaryData().pack(self.value))


class LLDP(GenericStruct):
    ethernet_header = Ethernet(type=35020)
    lldp_tlv_chassis_id = LLDP_TLV(type=1)
    lldp_tlv_port = LLDP_TLV(type=2)
    lldp_tlv_ttl = LLDP_TLV(type=3)
    # list_of_extra_tlvs = ListOfTLVs()
    lldp_tlv_end = LLDP_TLV(type=0, length=0, value=0)

    def __init__(self, source=None, tlvs=None):
        super().__init__()
        # 01-80-C2-00-00-00 or 01-80-C2-00-00-03 are also valid values for LLDP
        # multicast
        self.ethernet_header.destination = '01-80-C2-00-00-0E'
        self.ethernet_header.source = source
