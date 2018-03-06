"""Basic Network packet types.

Defines and Implements Basic Network packet types , such as Ethertnet and LLDP.
"""

# System imports
from copy import deepcopy
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, FixedTypeList, HWAddress, IPAddress, UBInt8, UBInt16)
from pyof.foundation.exceptions import PackException, UnpackException

__all__ = ('ARP', 'Ethernet', 'EtherType', 'GenericTLV', 'IPv4', 'VLAN',
           'TLVWithSubType', 'LLDP')


# NETWORK CONSTANTS AND ENUMS
class EtherType(IntEnum):
    """Enumeration with IEEE Ethernet types.

    The items are being added as we need.
    If you need one EtherType that is not listed below, please, send us a Pull
    Request with the addition.

    Ref: http://standards-oui.ieee.org/ethertype/eth.txt

    """

    #: Internet Protocol version 4 (IPv4)
    IPV4 = 0x0800
    #: Address Resolution Protocol (ARP)
    ARP = 0x0806
    #: Reverse Address Resolution Protocol
    RARP = 0x8035
    #: VLAN-tagged frame (IEEE 802.1Q) and Shortest Path Bridging IEEE 802.1aq
    #: with NNI compatibility[8]
    #: IEEE Std 802.1Q - Customer VLAN Tag Type
    VLAN = 0x8100
    #: Internet Protocol Version 6 (IPv6)
    IPV6 = 0x86DD
    #: Ethernet flow control
    ETHERNET_FLOW_CONTROL = 0x8808
    #: MPLS (multiprotocol label switching) label stack - unicast
    #: reference: RFC 3032 URL: ftp://ftp.rfc-editor.org/in-notes/rfc3032.txt
    MPLS_UNICAST = 0x8847
    #: MPLS (multiprotocol label switching) label stack - multicast
    #: reference: RFC 3032 URL: ftp://ftp.rfc-editor.org/in-notes/rfc3032.txt
    MPLS_MULTICAST = 0x8848
    #: Link Layer Discovery Protocol (LLDP)
    LLDP = 0x88CC
    #: VLAN-tagged (IEEE 802.1Q) frame with double tagging
    #: Std 802.1Q Service VLAN tag identifier
    VLAN_QINQ = 0x88a8


class ARP(GenericStruct):
    """ARP packet "struct".

    Contains fields for an ARP packet's header and data.
    Designed for Ethernet and IPv4 only: needs to have some attributes changed
    for other HTYPE and PTYPE implementations.
    Must be encapsulated inside an Ethernet frame.
    """

    htype = UBInt16()
    ptype = UBInt16()
    hlen = UBInt8()
    plen = UBInt8()
    oper = UBInt16()
    sha = HWAddress()
    spa = IPAddress()
    tha = HWAddress()
    tpa = IPAddress()

    def __init__(self, htype=1, ptype=EtherType.IPV4, hlen=6, plen=4, oper=1,
                 sha='00:00:00:00:00:00', spa='0.0.0.0',
                 tha="00:00:00:00:00:00", tpa='0.0.0.0'):
        """Create an ARP with the parameters below.

        Args:
            htype (int): Hardware protocol type. Defaults to 1 for Ethernet.
            ptype (int): Network protocol type. Defaults to 0x800 for IPv4.
            hlen (int): Length of the hardware address. Defaults to 6 for MAC
                        addresses.
            plen (int): Length of the networking protocol address. Defaults to
                        4 for IPv4 addresses.
            oper (int): Determines the operation for this ARP packet. Must be 1
                        for ARP request or 2 for ARP reply. Defaults to 1.
            sha (str): Sender hardware address. Defaults to
                       '00:00:00:00:00:00'.
            spa (str): Sender protocol address. Defaults to '0.0.0.0'.
            tha (str): Target hardware address. Defaults to
                       '00:00:00:00:00:00'.
            tpa (str): Target protocol address. Defaults to '0.0.0.0'.
        """
        super().__init__()
        self.htype = htype
        self.ptype = ptype
        self.hlen = hlen
        self.plen = plen
        self.oper = oper
        self.sha = sha
        self.spa = spa
        self.tha = tha
        self.tpa = tpa

    def is_valid(self):
        """Assure the ARP contains Ethernet and IPv4 information."""
        return self.htype == 1 and self.ptype == EtherType.IPV4

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Return the values instead of the lib's basic types.
        Check if the protocols involved are Ethernet and IPv4. Other protocols
        are currently not supported.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.

        """
        super().unpack(buff, offset)
        if not self.is_valid():
            raise UnpackException("Unsupported protocols in ARP packet")


class VLAN(GenericStruct):
    """802.1q VLAN header."""

    #: tpid (:class:`UBInt16`): Tag Protocol Identifier
    tpid = UBInt16(EtherType.VLAN)
    #: _tci (:class:`UBInt16`): Tag Control Information - has the
    #: Priority Code Point, DEI/CFI bit and the VLAN ID
    _tci = UBInt16()

    def __init__(self, pcp=None, cfi=None, vid=None):
        """Create a VLAN with the parameters below.

        If no arguments are set for a particular instance, it is interpreted as
        abscence of VLAN information, and the pack() method will return an
        empty binary string.

        Args:
            tpid (int): Tag Protocol Identifier. Defaults to 0x8100 for 802.1q.
            pcp (int): 802.1p Priority Code Point. Defaults to 0 for Best
                       Effort Queue.
            cfi (int): Canonical Format Indicator. Defaults to 0 for Ethernet.
            vid (int): VLAN ID. If no VLAN is specified, value is 0.
        """
        super().__init__()
        self.tpid = EtherType.VLAN
        self.pcp = pcp
        self.cfi = cfi
        self.vid = vid

    def pack(self, value=None):
        """Pack the struct in a binary representation.

        Merge some fields to ensure correct packing.

        If no arguments are set for a particular instance, it is interpreted as
        abscence of VLAN information, and the pack() method will return an
        empty binary string.

        Returns:
            bytes: Binary representation of this instance.

        """
        if isinstance(value, type(self)):
            return value.pack()

        if self.pcp is None and self.cfi is None and self.vid is None:
            return b''
        self.pcp = self.pcp if self.pcp is not None else 0
        self.cfi = self.cfi if self.cfi is not None else 0
        self.vid = self.vid if self.vid is not None else 0
        self._tci = self.pcp << 13 | self.cfi << 12 | self.vid
        return super().pack()

    def _validate(self):
        """Assure this is a valid VLAN header instance."""
        if self.tpid.value not in (EtherType.VLAN, EtherType.VLAN_QINQ):
            raise UnpackException
        return

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Return the values instead of the lib's basic types.

        After unpacking, the abscence of a `tpid` value causes the assignment
        of None to the field values to indicate that there is no VLAN
        information.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.

        """
        super().unpack(buff, offset)
        if self.tpid.value:
            self._validate()
            self.tpid = self.tpid.value
            self.pcp = self._tci.value >> 13
            self.cfi = (self._tci.value >> 12) & 1
            self.vid = self._tci.value & 4095
        else:
            self.tpid = EtherType.VLAN
            self.pcp = None
            self.cfi = None
            self.vid = None


class ListOfVLAN(FixedTypeList):
    """List of VLAN tags.

    Represented by instances of VLAN.
    """

    def __init__(self, items=None):
        """Create a ListOfVLAN with the optional parameters below.

        Args:
            items (:class:`~pyof.foundation.network_types.VLAN`):
                Instance or a list of instances.
        """
        super().__init__(pyof_class=VLAN, items=items)


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

    destination = HWAddress()
    source = HWAddress()
    vlans = ListOfVLAN()
    ether_type = UBInt16()
    data = BinaryData()

    def __init__(self, destination=None, source=None, vlans=None,
                 ether_type=None, data=b''):
        """Create an instance and set its attributes.

        Args:
            destination (:class:`~pyof.foundation.basic_types.HWAddress`):
                The final destination MAC address.
            source (:class:`~pyof.foundation.basic_types.HWAddress`):
                The source Mac address of the packet.
            ether_type (:class:`~pyof.foundation.basic_types.UBInt16`):
                The EtherType of packet.
            data (:class:`~pyof.foundation.basic_types.BinaryData`):
                The content of the packet in binary format.
        """
        super().__init__()
        self.destination = destination
        self.source = source
        self.vlans = ListOfVLAN() if vlans is None else vlans
        self.ether_type = ether_type
        self.data = data

    def get_hash(self):
        """Calculate a hash and returns it.

        Returns:
            int: Integer value that identifies this instance.

        """
        return hash(self.pack())

    @staticmethod
    def _get_vlan_length(buff):
        """Return the total length of VLAN tags in a given Ethernet buffer."""
        length = 0
        begin = 12

        while(buff[begin:begin+2] in (EtherType.VLAN.to_bytes(2, 'big'),
                                      EtherType.VLAN_QINQ.to_bytes(2, 'big'))):
            length += 4
            begin += 4

        return length

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results.

        Ethernet headers may have VLAN tags. If no VLAN tag is found, a
        'wildcard VLAN tag' is inserted to assure correct unpacking.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.

        Raises:
            UnpackException: If there is a struct unpacking error.

        """
        begin = offset

        vlan_length = self._get_vlan_length(buff)

        for attribute_name, class_attribute in self.get_class_attributes():
            attribute = deepcopy(class_attribute)
            if attribute_name == 'vlans':
                attribute.unpack(buff[begin:begin+vlan_length])
            else:
                attribute.unpack(buff, begin)
            setattr(self, attribute_name, attribute)
            begin += attribute.get_size()


class GenericTLV(GenericStruct):
    """TLV structure of LLDP packets.

    This is a Type, Length and Value (TLV) struct.

    The LLDP/TLV definition states that the Type field have 7 bits, while
    the length have 9 bits. The Value must be between 0-511 octets.

    Internally, on the instances of this class, the Type is a integer
    (0-127) and the Length is dynamically calculated based on the current
    type and value.
    """

    def __init__(self, tlv_type=127, value=None):
        """Create an instance and set its attributes.

        Args:
            tlv_type (int): Type used by this class. Defaults to 127.
            value (:class:`~pyof.foundation.basic_types.BinaryData`):
                Value stored by GenericTLV.
        """
        super().__init__()
        self.tlv_type = tlv_type
        self._value = BinaryData() if value is None else value

    @property
    def value(self):
        """Return the value stored by GenericTLV.

        Returns:
            :class:`~pyof.foundation.basic_types.BinaryData`:
                Value stored by GenericTLV.

        """
        return self._value

    @property
    def length(self):
        """Return the length of value stored by GenericTLV.

        Returns:
            int: Value length in bytes.

        """
        return len(self.value.pack())

    @property
    def header(self):
        """Header of the TLV Packet.

        The header is composed by the Type (7 bits) and Length (9 bits),
        summing up 16 bits. To achieve that, we need to do some bitshift
        operations.

        Returns:
            :class:`~pyof.foundation.basic_types.UBInt16`:
                Result after all operations.

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

    def unpack(self, buff, offset=0):
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
        header.unpack(buff[offset:offset+2])
        self.tlv_type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        self._value = BinaryData(buff[begin:end])

    def get_size(self, value=None):
        """Return struct size.

        Returns:
            int: Returns the struct size based on inner attributes.

        """
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

    def __init__(self, version=4, ihl=5, dscp=0, ecn=0, length=0,
                 identification=0, flags=0, offset=0, ttl=255, protocol=0,
                 checksum=0, source="0.0.0.0", destination="0.0.0.0",
                 options=b'', data=b''):
        """Create an IPv4 with the parameters below.

        Args:
            version (int): IP protocol version. Defaults to 4.
            ihl (int): Internet Header Length. Default is 5.
            dscp (int): Differentiated Service Code Point. Defaults to 0.
            ecn (int): Explicit Congestion Notification. Defaults to 0.
            length (int): IP packet length in bytes. Defaults to 0.
            identification (int): Packet Id. Defaults to 0.
            flags (int): IPv4 Flags. Defults 0.
            offset (int): IPv4 offset. Defaults to 0.
            ttl (int): Packet time-to-live. Defaults to 255
            protocol (int): Upper layer protocol number. Defaults to 0.
            checksum (int): Header checksum. Defaults to 0.
            source (str): Source IPv4 address. Defaults to "0.0.0.0"
            destination (str): Destination IPv4 address. Defaults to "0.0.0.0"
            options (bytes): IP options. Defaults to empty bytes.
            data (bytes): Packet data. Defaults to empty bytes.
        """
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

        Returns:
            bytes: Binary representation of this instance.

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

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.

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
    specific structure, with the :attr:`value` field being splitted into a
    :attr:`sub_type` field and a new :attr:`sub_value` field.
    """

    def __init__(self, tlv_type=1, sub_type=7, sub_value=None):
        """Create an instance and set its attributes.

        Args:
            tlv_type (int): Type used by this class. Defaults to 1.
            sub_type (int): Sub type value used by this class. Defaults to 7.
            sub_value (:class:`~pyof.foundation.basic_types.BinaryData`):
                Data stored by TLVWithSubType. Defaults to empty BinaryData.
        """
        super().__init__(tlv_type)
        self.sub_type = sub_type
        self.sub_value = BinaryData() if sub_value is None else sub_value

    @property
    def value(self):
        """Return sub type and sub value as binary data.

        Returns:
            :class:`~pyof.foundation.basic_types.BinaryData`:
                BinaryData calculated.

        """
        binary = UBInt8(self.sub_type).pack() + self.sub_value.pack()
        return BinaryData(binary)

    def unpack(self, buff, offset=0):
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
        header.unpack(buff[offset:offset+2])
        self.tlv_type = header.value >> 9
        length = header.value & 511
        begin, end = offset + 2, offset + 2 + length
        sub_type = UBInt8()
        sub_type.unpack(buff[begin:begin+1])
        self.sub_type = sub_type.value
        self.sub_value = BinaryData(buff[begin+1:end])


class LLDP(GenericStruct):
    """LLDP class.

    Build a LLDP packet with TLVSubtype and Generic Subtypes.

    It contains a chassis_id TLV, a port_id TLV, a TTL (Time to live) and
    another TLV to represent the end of the LLDP Packet.
    """

    #: chassis_id (:class:`~TLVWithSubType`) with tlv_type = 1 and sub_type = 7
    chassis_id = TLVWithSubType(tlv_type=1, sub_type=7)
    #: port_id (:class:`TLVWithSubType`) with tlv = 2 and sub_type = 7
    port_id = TLVWithSubType(tlv_type=2, sub_type=7)
    #: TTL (:class:`GenericTLV`) time is given in seconds, between 0 and 65535,
    #: with tlv_type = 3
    ttl = GenericTLV(tlv_type=3, value=UBInt16(120))
    # We are not using list of tlvs for now
    # tlvs = ListOfTLVs()
    #: end (:class:`GenericTLV`) with tlv_type = 0
    end = GenericTLV(tlv_type=0)
