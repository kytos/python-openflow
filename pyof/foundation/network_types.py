"""Basic Network packet types.

Defines and Implements Basic Network packet types , such as Ethertnet and LLDP.
"""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import BinaryData, HWAddress, UBInt8, UBInt16
from pyof.foundation.exceptions import PackException

__all__ = ('Ethernet', 'GenericTLV', 'TLVWithSubType', 'LLDP')


class Ethernet(GenericStruct):
    """Ethernet "struct".

    Objects of this class represents an ethernet packet. It contains the
    'Ethernet header', composed by destination (MAC), source (MAC), type
    (EtherType)[1] and the payload of the packet, as binary data.

    This class does not consider the Ethernet 'Preamble' or the 'CRC'.

    There is also a get_hash method, that hashes the binary representation of
    the object so we can have a unique representation of the ethernet packet,
    so we can keep a track of ethernet packets being flooded over the network.

    [1] EtherTypes:
    http://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml#ieee-802-numbers-1
    """

    #: destination (:class:`HWAddress`): The final destination MAC address.
    destination = HWAddress()
    #: source (:class:`HWAddress`): The source MAC address of the packet.
    source = HWAddress()
    #: ether_type (:class:`UBInt16`): The EtherType of the packet.
    ether_type = UBInt16()
    #: data (:class:`BinaryData`): The content of the packet in binary format.
    data = BinaryData()

    def __init__(self, destination=None, source=None, ether_type=None,
                 data=b''):
        """Create an instance and set its attributes."""
        super().__init__()
        self.destination = destination
        self.source = source
        self.ether_type = ether_type
        self.data = data

    def get_hash(self):
        """Return a hash that identifies this instance."""
        return hash(self.pack())


class GenericTLV(GenericStruct):
    """TLV structure of LLDP packets.

    This is a Type, Length and Value (TLV) struct.

    The LLDP/TLV definition states that the Type field have 7 bits, while
    the length have 9 bits. The Value must be between 0-511 octets.

    Internally, on the instances of this class, the Type is a integer
    (0-127) and the Length is dynamically calculated based on the current
    type and value.
    """

    def __init__(self, tlv_type=127, value=BinaryData()):
        """Create an instance and set its attributes."""
        super().__init__()
        self.tlv_type = tlv_type
        self._value = value

    @property
    def value(self):
        """Return the value stored by GenericTLV."""
        return self._value

    @property
    def length(self):
        """Struct length in bytes."""
        return len(self.value.pack())

    @property
    def header(self):
        """Header of the TLV Packet.

        The header is composed by the Type (7 bits) and Length (9 bits),
        summing up 16 bits. To achieve that, we need to do some bitshift
        operations.
        """
        return UBInt16(((self.tlv_type & 127) << 9) | (self.length & 511))

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
        self.tlv_type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        self._value = BinaryData(buffer[begin:end])

    def get_size(self, value=None):
        """Return struct size."""
        if isinstance(value, type(self)):
            return value.get_size()

        return 2 + self.length


class TLVWithSubType(GenericTLV):
    """Modify the :class:`GenericTLV` to a Organization Specific TLV structure.

    Beyond the standard TLV (type, length, value), we can also have a more
    specific structure, with the *value* field being splitted into a *sub_type*
    field and a new "*sub_value*" field.
    """

    def __init__(self, tlv_type=1, sub_type=7, sub_value=BinaryData()):
        """Create an instance and set its attributes."""
        super().__init__(tlv_type)
        self.sub_type = sub_type
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
        self.tlv_type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        sub_type = UBInt8()
        sub_type.unpack(buffer[begin:begin+1])
        self.sub_type = sub_type.value
        self.sub_value = BinaryData(buffer[begin+1:end])


class LLDP(GenericStruct):
    """LLDP class.

    Build a LLDP packet with TLVSubtype and Generic Subtypes.

    It contains a chassis_id TLV, a port_id TLV, a TTL (Time to live) and
    another TVL to represent the end of the LLDP Packet.
    """

    chassis_id = TLVWithSubType(tlv_type=1, sub_type=7)
    port_id = TLVWithSubType(tlv_type=2, sub_type=7)
    #: TTL time is given in seconds, between 0 and 65535
    ttl = GenericTLV(tlv_type=3, value=UBInt16(120))
    # We are not using list of tlvs for now
    # tlvs = ListOfTLVs()
    end = GenericTLV(tlv_type=0)
