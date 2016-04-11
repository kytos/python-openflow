"""Defines Header classes and related items"""

# System imports
import enum
import struct

# Third-party imports

# Local source tree imports
from ofp.v0x02.foundation import base
from ofp.v0x02.foundation import basic_types


class OFPType(enum.Enum):
    """Enumeration of Message Types"""
    # Symetric/Immutable messages
    OFPT_HELLO = basic_types.UBInt8(0)
    OFPT_ERROR = basic_types.UBInt8(1)
    OFPT_ECHO_REQUEST = basic_types.UBInt8(2)
    OFPT_ECHO_REPLY = basic_types.UBInt8(3)
    OFPT_VENDOR = basic_types.UBInt8(4)

    # Switch configuration messages
    # Controller/Switch messages
    OFPT_FEATURES_REQUEST = basic_types.UBInt8(5)
    OFPT_FEATURES_REPLY = basic_types.UBInt8(6)
    OFPT_GET_CONFIG_REQUEST = basic_types.UBInt8(7)
    OFPT_GET_CONFIG_REPLY = basic_types.UBInt8(8)
    OFPT_SET_CONFIG = basic_types.UBInt8(9)

    # Async messages
    OFPT_PACKET_IN = basic_types.UBInt8(10)
    OFPT_FLOW_REMOVED = basic_types.UBInt8(11)
    OFPT_PORT_STATUS = basic_types.UBInt8(12)

    # Controller command messages
    # Controller/switch message
    OFPT_PACKET_OUT = basic_types.UBInt8(13)
    OFPT_FLOW_MOD = basic_types.UBInt8(14)
    OFPT_PORT_MOD = basic_types.UBInt8(15)

    # Statistics messages
    # Controller/Switch message
    OFPT_STATS_REQUEST = basic_types.UBInt8(16)
    OFPT_STATS_REPLY = basic_types.UBInt8(17)

    # Barrier messages
    # Controller/Switch message
    OFPT_BARRIER_REQUEST = basic_types.UBInt8(18)
    OFPT_BARRIER_REPLY = basic_types.UBInt8(19)

    # Queue Configuration messages
    # Controller/Switch message
    OFPT_QUEUE_GET_CONFIG_REQUEST = basic_types.UBInt8(20)
    OFPT_QUEUE_GET_CONFIG_REPLY = basic_types.UBInt8(21)

    @classmethod
    def get_size(cls):
        """ Return the size of enumerator internal value type in bytes """
        return struct.calcsize("!B")


class OFPHeader(base.GenericStruct):
    """Representation of an OpenFlow message Header

        :param ofp_type: Type of  the message
        :param length:   Length of the message, including the header itself
        :param xid:      id of the message
    """
    version = basic_types.UBInt8()
    ofp_type = basic_types.UBInt8()
    length = basic_types.UBInt16()
    xid = basic_types.UBInt32()

    def __init__(self,
                 ofp_type=OFPType.OFPT_HELLO,
                 length=basic_types.UBInt16(0),
                 xid=basic_types.UBInt32(0)):
        self.version = basic_types.UBInt8(base.OFP_VERSION)
        self.ofp_type = ofp_type
        self.length = length
        self.xid = xid

    def _field(self, fieldName):
        return getattr(self, fieldName)
