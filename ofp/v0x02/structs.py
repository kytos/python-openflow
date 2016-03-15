from ofp.v0x02.types import UBInt8, UBInt8Array, UBInt16, UBInt32, Char
from ofp.v0x02.exceptions import OFPException
from ofp.v0x02.enums import OFPActionType
from ofp.v0x02.consts import *

import collections

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
                hex += getattr(self, _attr).build()
                print("{} {} {}".
                      format(_attr, attr,getattr(self, _attr).build()))
            elif not callable(attr):
                hex += _class(attr).build()
                print("{} {} {}"
                      .format(_attr, attr,_class(attr).build()))
        return hex

    def unpack(self, buff):
        begin = 0
        for _attr, _class in self.__ordered__:
            attr = getattr(self, _attr)
            if _class is OFPHeader:
                size = (getattr(self, _attr).get_size())
                getattr(self,_attr).parse(buff, offset=begin)
            elif not callable(attr):
                size = (_class(attr).get_size())
                getattr(self,_attr).parse(buff, offset=begin)
            begin += size


class OFPHeader(GenericStruct):
    version = UBInt8()
    ofp_type = UBInt8()
    length = UBInt16()
    xid = UBInt32()


class OFPPhyPort(metaclass=GenericStruct):
    """
    Description of a physical port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    OFP_MAX_ETH_ALEN is 6. The name field is a null-terminated string
    containing a human-readable name for the interface. The value of
    OFP_MAX_PORT_NAME_LEN is 16.
    """
    _build_order=('port_no', 'hw_addr', 'name', 'config', 'state', 'curr',
                  'advertised', 'supported', 'peer')

    # Attributes
    port_no = UBInt16()
    hw_addr = UBInt8Array(length = OFP_ETH_ALEN)
    name = Char(length = OFP_MAX_PORT_NAME_LEN)
    config = UBInt32()      # Bitmap of OFPPC* flags
    state = UBInt32()       # Bitmap of OFPPS* flags

    # Bitmaps of OFPPF_* that describe features. All bits zeroed if
    # unsupported or unavailable.
    curr = UBInt32()        # Current features
    advertised = UBInt32()  # Features being advertised by the port
    supported = UBInt32()   # Features supported by the port
    peer = UBInt32()        # Features advertised by peer


# TODO: Queue structs. 5.2.2 in specification.


class OFPMatch(GenericStruct):
    """ Flow entry. """

    _build_order=('wildcards', 'in_port', 'dl_src', 'dl_dst', 'dl_vlan',
                  'dl_vlan_pcp', 'pad1', 'dl_type', 'nw_tos', 'nw_proto',
                  'pad2', 'nw_src', 'nw_dst', 'tp_src', 'tp_dst')

    wildcards = UBInt32()                       # Wildcard fields
    in_port = UBInt16()                         # Input switch port
    dl_src = UBInt8Array(length = OFP_ETH_ALEN) # Ethernet source address
    dl_dst = UBInt8Array(length = OFP_ETH_ALEN) # Ethernet destination address
    dl_vlan = UBInt16()                         # Input VLAN ID
    dl_vlan_pcp = UBInt8()                      # Input VLAN priority
    pad1 = UBInt8Array(length = 1)              # Align to 64-bits
    dl_type = UBInt16()                         # Ethernet frame type
    nw_tos = UBInt8()                           # IP ToS (actually DSCP field,
                                                # 6bits).
    nw_proto = UBInt8()                         # IP protocol or lower 8 bits of
                                                # ARP opcode
    pad2 = UBInt8Array(length = 2)              # Align to 64-bits
    nw_src = UBInt32()                          # IP Source address
    nw_dst = UBInt32()                          # IP Destination address
    tp_src = UBInt16()                          # TCP/UDP source port
    tp_dst = UBInt16()                          # TCP/UDP destination port


class OFPActionOutput(GenericStruct):
    """
    Action structure for OFPAT_OUTPUT, which sends packets out 'port'.
    When the 'port' is the OFPP_CONTROLLER, 'max_len' indicates the max
    number of bytes to send. A 'max_len' of zero means no bytes of the
    packet should be sent.

    The port specifies the physical port from which packets should be sent.
    """
    _build_order = ('type', 'len', 'port', 'max_len')

    # Attributes
    type = UBInt16(OFPActionType.OFPAT_OUTPUT)  # OFPAT_OUTPUT
    len = UBInt16(8)                            # Length is 8.
    port = UBInt16()                            # Output port
    max_len = UBInt16()                         # Max length to send to
                                                # controller.

# TODO: Action enqueue.


class OFPActionVlanVid(GenericStruct):
    """
    If no VLAN is present, a new header is added with the specified VLAN ID and
    priority of zero. If a VLAN header already exists, the VLAN ID is replaced
    with the specified value.

    The vlan_vid field is 16 bits long, when an actual VLAN id is only 12 bits.
    The value 0xffff is used to indicate that no VLAN id was set
    """
    _build_order = ('type', 'len', 'vlan_vid', 'pad')

    # Attributes
    type = UBInt16(OFPActionType.OFPAT_SET_VLAN_VID)  # OFPAT_SET_VLAN_VID
    len = UBInt16(8)                                  # Length is 8.
    vlan_vid = UBInt16()                              # VLAN id
    pad = UBInt8Array(length=2)


class OFPActionVlanPcp(GenericStruct):
    """
    Change VLAN priority.

    If no VLAN is present, a new header is added with the specified priority and
    a VLAN ID of zero. If a VLAN header already exists, the priority field is
    replaced with the specified value.

    The vlan_pcp field is 8 bits long, but only the lower 3 bits have meaning.

    """
    _build_order = ('type', 'len', 'vlan_pcp', 'pad')

    # Attributes
    type = UBInt16(OFPActionType.OFPAT_SET_VLAN_PCP)  # OFPAT_SET_VLAN_PCP
    len = UBInt16(8)                                  # Length is 8.
    vlan_pcp = UBInt16()                              # VLAN priority
    pad = UBInt8Array(length=3)


class OFPActionStripVlan(GenericStruct):
    """
    This action strips the VLAN tag if one is present.

    An action_strip_vlan takes no arguments and consists only of a generic
    ofp_action_header.
    """
    _build_order = ('type', 'len', 'pad')

    # Attributes
    type = UBInt16(OFPActionType.OFPAT_STRIP_VLAN)    # OFPAT_STRIP_VLAN
    len = UBInt16(8)                                  # Length is 8
    pad = UBInt8Array(length=4)


class OFPActionDLAddr(GenericStruct):
    """
    Action structure for OFPAT_SET_DL_SRC/DST.

    The dl_addr field is the MAC address to set.
    """
    _build_order = ('type', 'len', 'dl_addr', 'pad')

    # Attributes
    type = UBInt16()                                  # OFPAT_SET_DL_SRC/DST
    len = UBInt16(16)                                 # Length is 16
    dl_addr = UBInt8Array(length=OFP_ETH_ALEN)        # Ethernet Address
    pad = UBInt8Array(length=6)


class OFPActionNWAddr(GenericStruct):
    """
    Action structure for OFPAT_SET_NW_SRC/DST.

    The nw_addr field is the IP address to set.
    """
    _build_order = ('type', 'len', 'nw_addr')

    # Attributes
    type = UBInt16()                                  # OFPAT_SET_NW_SRC/DST
    len = UBInt16(8)                                  # Length is 8
    nw_addr = UBInt32()                               # IP Address


class OFPActionNWTOS(GenericStruct):
    """
    Action structure for OFPAT_SET_NW_TOS.

    The nw_tos field is the 6 upper bits of the ToS field to set, in the
    original bit positions (shifted to the left by 2).
    """
    _build_order = ('type', 'len', 'nw_tos', 'pad')

    # Attributes
    type = UBInt16(OFPActionType.OFPAT_SET_NW_TOS)    # OFPAT_SET_NW_TOS
    len = UBInt16(8)                                  # Length is 8
    nw_tos = UBInt8()                                 # IP ToS (DSCP Field,6bits)
    pad = UBInt8Array(length=3)


class OFPActionTPPort(GenericStruct):
    """
    Action structure for OFPAT_SET_TP_SRC/DST.

    The tp_port field is the TCP/UDP/other port to set.
    """
    _build_order = ('type', 'len', 'tp_port', 'pad')

    # Attributes
    type = UBInt16()                                  # OFPAT_SET_TP_SRC/DST
    len = UBInt16(8)                                  # Length is 8
    tp_port = UBInt16()                               # TCP/UDP Port
    pad = UBInt8Array(length=2)


class OFPActionVendorHeader(GenericStruct):
    """
    Action structure for OFPAT_VENDOR.

    The rest of the body is vendor-defined.
    """
    _build_order = ('type', 'len', 'tp_port', 'pad')

    # Attributes
    type = UBInt16()                                  # OFPAT_SET_TP_SRC/DST
    len = UBInt16(8)                                  # Length is always
                                                      # multiple of 8.
    vendor = UBInt32()                                # Vendor ID,  which takes
                                                      # the same form as in


class OFPPacketIn(GenericStruct):
    _build_order = ()

    # Attributes
    #header = OFPHeader()
    buffer_id = UBInt32()
    total_len = UBInt16()
    in_port = UBInt16()
    reason = UBInt8()
    pad = UBInt8()
