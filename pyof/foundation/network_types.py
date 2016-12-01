"""Basic Network Types."""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import BinaryData, HWAddress, UBInt8, UBInt16
from pyof.foundation.exceptions import PackException

__all__ = ('Ethernet', 'GenericTLV', 'TLVWithSubType', 'LLDP')


class Ethernet(GenericStruct):
    """Ethernet struct."""

    destination = HWAddress()
    source = HWAddress()
    type = UBInt16()
    data = BinaryData()

    def __init__(self, destination=None, source=None, eth_type=None, data=b''):
        """Create an instance and set its attributes."""
        super().__init__()
        self.destination = destination
        self.source = source
        self.type = eth_type
        self.data = data

    def get_hash(self):
        """Return a hash that identifies this instance."""
        return hash(self.pack())


class GenericTLV:
    """TLV structure of LLDP packets.

    This is a Type, Length and Value struct.
    """

    def __init__(self, tlv_type=127, value=BinaryData()):
        """Create an instance and set its attributes."""
        self.type = tlv_type
        self._value = value

    @property
    def value(self):
        """Return TLV value."""
        return self._value

    @property
    def length(self):
        """Struct length in bytes."""
        return len(self.value.pack())

    @property
    def header(self):
        """Header."""
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
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            Exception: If there is a struct unpacking error.
        """
        header = UBInt16()
        header.unpack(buffer[offset:offset+2])
        self.type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        self.value = BinaryData(buffer[begin:end])

    def get_size(self, value=None):
        """Return struct size."""
        if isinstance(value, type(self)):
            return value.get_size()
        else:
            return 2 + self.length


class TLVWithSubType(GenericTLV):
    """Add sub type and sub value to :class:`GenericTLV` and remove value."""

    def __init__(self, tlv_type=1, sub_type=7, sub_value=None):
        """Create an instance and set its attributes."""
        super().__init__(tlv_type=tlv_type)
        self.sub_type = sub_type
        if sub_value is None:
            sub_value = BinaryData()
        self.sub_value = sub_value

    @property
    def value(self):
        """Return sub type and sub value as binary data."""
        binary = UBInt8(self.sub_type).pack() + self.sub_value.pack()
        return BinaryData(binary)

    def unpack(self, buffer, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            Exception: If there is a struct unpacking error.
        """
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

    chassis_id = TLVWithSubType(tlv_type=1, sub_type=7)
    port_id = TLVWithSubType(tlv_type=2, sub_type=7)
    #: TTL time is given in seconds, between 0 and 65535
    ttl = GenericTLV(tlv_type=3, value=UBInt16(120))
    end = GenericTLV(tlv_type=0)
