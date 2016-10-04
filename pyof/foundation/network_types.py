"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import BinaryData, HWAddress, UBInt8, UBInt16

__all__ = ('Ethernet', 'LLDP', 'LLDP_TLV')


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
    type = UBInt8
    #: Defines the length of subtype + value
    length = UBInt8()
    value = BinaryData()

    def __init__(self, type, length, subtype, value=None):
        self.type = type
        self.length = length
        self.value = value if value is not None else b''

    def _type_is_valid(self):
        """Check if the type value can be represented in 7 bits."""
        # 7 bits can represent 128 values, from 0 to 127.
        if self.type > 0 and self.type < 128:
            return True
        else:
            return False

    def _length_is_valid(self):
        """Check if the length value can be represented in 9 bits."""
        # 9 bits can represent 512 values, from 0 to 511
        if self.length > 0 and self.length < 511:
            return True
        else:
            return False

    def update_length(self):
        """Updates the length attribute of the instance."""
        pass

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
            output += UBInt8().pack(self.length & ((1 << 8) -1))
            output += self.value.pack()

            return output
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buffer, offset=0):
        being = offset
        end = offset + 16
        type_and_length = UBInt16().unpack(buffer[begin:end]).value
        self.type = type_and_length >> 9
        self.length = type_and_length & ((1 << 10) - 1)
        begin = end
        end = end + length
        self.data = BinaryData().unpack(buffer[begin:end])


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
