"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (BinaryData, FixedTypeList, HWAddress,
                                         UBInt8, UBInt16, UBInt64)

from pyof.foundation.exceptions import PackException

__all__ = ('Ethernet', 'LLDP', 'LLDP_TLV', 'ListOfTLVs')


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

    def __init__(self, type, value=0):
        self.type = type
        self.value = value

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
        begin = offset
        end = begin + 2
        type_and_length = UBInt16()
        type_and_length.unpack(buffer[begin:end])
        self.type = type_and_length.value >> 9
        self.length = type_and_length.value & ((1 << 10) - 1)
        begin = end
        end += self.length
        self.value = BinaryData()
        self.value.unpack(buffer[begin:end])

    def get_size(self, value=None):
        if isinstance(value, type(self)):
            return value.get_size()
        else:
            return 2 + len(BinaryData().pack(self.value))


class ListOfTLVs(FixedTypeList):
    """List of instances of LLDP_TLV class.

    Represented by instances of LLDP_TLV and used on :class:`LLDP` objects.
    """

    def __init__(self, items=None):
        """The constructor takes the option paramenter below.

        Args: items(:class:`list`, :class:`LLDP_TLV`): One :class:`LLDP_TLV`
            instance or list.
        """
        super().__init__(pyof_class=LLDP_TLV,
                         items=items)


class LLDP(GenericStruct):
    """LLDP class."""

    ethernet_header = Ethernet(type=35020)
    tlv_chassis_id = LLDP_TLV(type=1)
    tlv_port_id = LLDP_TLV(type=2)
    #: TTL time is given in seconds, between 0 and 65535
    tlv_ttl = LLDP_TLV(type=3)
    extra_tlvs = ListOfTLVs()
    tlv_end = LLDP_TLV(type=0, value=0)

    def __init__(self, source=None, chassis_id=None, port_id=None, ttl=30,
                 extra_tlvs=None):
        super().__init__()
        # 01-80-C2-00-00-00 or 01-80-C2-00-00-03 are also valid values for LLDP
        # multicast
        self.ethernet_header.destination = '01:80:C2:00:00:0E'
        self.ethernet_header.source = source
        #: For TLV_chassis_id we are using subtype 6 (InterfaceName) and
        #: passing, for now, the switch dpid. And the datapath_id of the
        #: switches are defined as UBInt64 on the OpenFlow spec (v0x01).
        self.tlv_chassis_id.value = b'\x06'
        if chassis_id is not None:
            self.tlv_chassis_id.value += UBInt64().pack(chassis_id)
        #: For TLV_port_id we are using subtype 5 (InterfaceName) and
        #: passing, for now, the port_no.
        self.tlv_port_id.value = b'\x05'
        if port_id is not None:
            self.tlv_port_id.value += UBInt16().pack(port_id)
        self.tlv_ttl.value = UBInt16().pack(ttl)
        self.extra_tlvs = [] if extra_tlvs is None else extra_tlvs
