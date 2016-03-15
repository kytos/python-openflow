from ofp.v0x02.structs import GenericStruct, OFPHeader
from ofp.v0x02.enums import OFPType
from ofp.v0x02.consts import OFP_VERSION
from ofp.v0x02.types import *


class GenericMessage(GenericStruct):
    def __init__(self, header, *args, **kwargs):
        """Receives the header and update the length field in it"""
        super().__init__(*args, **kwargs)
        self.header = header
        self.header.length = self.get_size()


class OFPHello(GenericMessage):
    header = OFPHeader(version = 1 , xid = 10, ofp_type=0, length=2)
    x = UBInt32()

    def __init__(self, xid = 0, x = 0):
        header = OFPHeader(version = 1 , xid = xid, ofp_type=2, length=0)
        self.x = x
        super(OFPHello, self).__init__(header)


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
