from enum import Enum
from ofp.v0x02.structs import GenericStruct, OFPHeader
from ofp.v0x02.consts import OFP_VERSION
from ofp.v0x02.of_basic_types import UBInt32


class OFPType(Enum):
    """
    Message Type
    """
    # Symetric/Immutable messages
    OFPT_HELLO = 0
    OFPT_ERROR = 1
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_VENDOR = 4

    # Switch configuration messages
    # Controller/Switch messages
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_GET_CONFIG_REQUEST = 7
    OFPT_GET_CONFIG_REPLY = 8
    OFPT_SET_CONFIG = 9

    # Async messages
    OFPT_PACKET_IN = 10
    OFPT_FLOW_REMOVED = 11
    OFPT_PORT_STATUS = 12

    # Controller command messages
    # Controller/switch message
    OFPT_PACKET_OUT = 13
    OFPT_FLOW_MOD = 14
    OFPT_PORT_MOD = 15

    # Statistics messages
    # Controller/Switch message
    OFPT_STATS_REQUEST = 16
    OFPT_STATS_REPLY = 17

    # Barrier messages
    # Controller/Switch message
    OFPT_BARRIER_REQUEST = 18
    OFPT_BARRIER_REPLY = 19

    # Queue Configuration messages
    # Controller/Switch message
    OFPT_QUEUE_GET_CONFIG_REQUEST = 20
    OFPT_QUEUE_GET_CONFIG_REPLY = 21


class GenericMessage(GenericStruct):
    def __init__(self, header, *args, **kwargs):
        """Receives the header and update the length field in it"""
        super().__init__(*args, **kwargs)
        self.header = header
        self.header.length = self.get_size()


class OFPHello(GenericMessage):
    header = OFPHeader(version = 2 , xid = 10, ofp_type=0, length=2)
    x = UBInt32()

    def __init__(self, xid = 0, x = 3):
        header = OFPHeader(version = 2 , xid = xid, ofp_type=0, length=0)
        self.x = x
        super(OFPHello, self).__init__(header)


class OFPFeaturesRequest(GenericMessage):
    header = OFPHeader(version = 2, xid = 10, ofp_type = 5, lenght=2)
    x = UBInt32()

    def __init__(self, xid = 0, x = 3):
        header = OFPHeader(version = 2 , xid = xid, ofp_type=5, length=0)
        self.x = x
        super(OFPFeaturesRequest, self).__init__(header)




#class OFPECHORequest(GenericMessage):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.lenght(self.get_size())
#        _msg_type = OFPType.OFPT_ECHO_REQUEST
#        _build_order = ('header', 'x')
#
#        header = OFPHeader(type = _msg_type, length = _length)
#        x = UBInt8()
#
#
#class OFPECHOReply(GenericMessage):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.lenght(self.get_size())
#        _msg_type = OFPType.OFPT_ECHO_REPLY
#        _build_order = ('header', 'x')
#
#        header = OFPHeader(type = _msg_type, length = _length)
#        x = UBInt8()
