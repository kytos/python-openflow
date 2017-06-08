"""Basic Network packet types.

Defines and Implements Basic Network packet types , such as Ethertnet and LLDP.
"""

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, HWAddress, IPAddress, UBInt8, UBInt16)
from pyof.foundation.exceptions import PackException

__all__ = ('Ethernet', 'GenericTLV', 'IPv4', 'TLVWithSubType', 'LLDP')


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


class IPv4(GenericStruct):
    """IPv4 packet "struct".

    Contains all fields of an IP version 4 packet header, plus the upper layer
    content as binary data.
    Some of the fields were merged together because of their size being
    inferior to 8 bits. They are represented as a single class attribute, but
    pack/unpack methods will take into account the values in individual
    instance attributes.
    """

    #: _version_ihl (:class:`UBInt8`): IP protocol version + Internet Header
    #: Length (words)
    _version_ihl = UBInt8()
    #: _dscp_ecn (:class:`UBInt8`): Differentiated Services Code Point
    #: (ToS - Type of Service) + Explicit Congestion Notification
    _dscp_ecn = UBInt8()
    #: length (:class:`UBInt16`): IP packet length (bytes)
    length = UBInt16()
    #: identification (:class:`UBInt16`): Packet ID - common to all fragments
    identification = UBInt16()
    #: _flags_offset (:class:`UBInt16`): Fragmentation flags + fragmentation
    #: offset
    _flags_offset = UBInt16()
    #: ttl (:class:`UBInt8`): Packet time-to-live
    ttl = UBInt8()
    #: protocol (:class:`UBInt8`): Upper layer protocol number
    protocol = UBInt8()
    #: checksum (:class:`UBInt16`): Header checksum
    checksum = UBInt16()
    #: source (:class:`IPAddress`): Source IPv4 address
    source = IPAddress()
    #: destination (:class:`IPAddress`): Destination IPv4 address
    destination = IPAddress()
    #: options (:class:`BinaryData`): IP Options - up to 320 bits, always
    #: padded to 32 bits
    options = BinaryData()
    #: data (:class:`BinaryData`): Packet data
    data = BinaryData()

    def __init__(self, version=4, ihl=5, dscp=0, ecn=0, length=0, # noqa
                 identification=0, flags=0, offset=0, ttl=255, protocol=0,
                 checksum=0, source="0.0.0.0", destination="0.0.0.0",
                 options=b'', data=b''):
        """Create the Packet and set instance attributes."""
        super().__init__()
        self.version = version
        self.ihl = ihl
        self.dscp = dscp
        self.ecn = ecn
        self.length = length
        self.identification = identification
        self.flags = flags
        self.offset = offset
        self.ttl = ttl
        self.protocol = protocol
        self.checksum = checksum
        self.source = source
        self.destination = destination
        self.options = options
        self.data = data

    def _update_checksum(self):
        """Update the packet checksum to enable integrity check."""
        source_list = [int(octet) for octet in self.source.split(".")]
        destination_list = [int(octet) for octet in
                            self.destination.split(".")]
        source_upper = (source_list[0] << 8) + source_list[1]
        source_lower = (source_list[2] << 8) + source_list[3]
        destination_upper = (destination_list[0] << 8) + destination_list[1]
        destination_lower = (destination_list[2] << 8) + destination_list[3]

        block_sum = ((self._version_ihl << 8 | self._dscp_ecn) + self.length +
                     self.identification + self._flags_offset +
                     (self.ttl << 8 | self.protocol) + source_upper +
                     source_lower + destination_upper + destination_lower)

        while block_sum > 65535:
            carry = block_sum >> 16
            block_sum = (block_sum & 65535) + carry

        self.checksum = ~block_sum & 65535

    def pack(self, value=None):
        """Pack the struct in a binary representation.

        Merge some fields to ensure correct packing.
        """
        # Set the correct IHL based on options size
        if self.options:
            self.ihl += int(len(self.options) / 4)

        # Set the correct packet length based on header length and data
        self.length = int(self.ihl * 4 + len(self.data))

        self._version_ihl = self.version << 4 | self.ihl
        self._dscp_ecn = self.dscp << 2 | self.ecn
        self._flags_offset = self.flags << 13 | self.offset

        # Set the checksum field before packing
        self._update_checksum()

        return super().pack()

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Return the values instead of the lib's basic types.
        """
        super().unpack(buff, offset)

        self.version = self._version_ihl.value >> 4
        self.ihl = self._version_ihl.value & 15
        self.dscp = self._dscp_ecn.value >> 2
        self.ecn = self._dscp_ecn.value & 3
        self.length = self.length.value
        self.identification = self.identification.value
        self.flags = self._flags_offset.value >> 13
        self.offset = self._flags_offset.value & 8191
        self.ttl = self.ttl.value
        self.protocol = self.protocol.value
        self.checksum = self.checksum.value
        self.source = self.source.value
        self.destination = self.destination.value

        if self.ihl > 5:
            options_size = (self.ihl - 5) * 4
            self.data = self.options.value[options_size:]
            self.options = self.options.value[:options_size]
        else:
            self.data = self.options.value
            self.options = b''


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
