from ofp.v0x01.structs import GenericStruct, OFPHeader
from ofp.v0x01.enums import OFPType
from ofp.v0x01.consts import OFP_VERSION
from ofp.v0x01.types import *

class OFPHELLO(GenericStruct):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = self.get_size()
    _msg_type = OFPType.OFPT_HELLO
    _build_order = ('header', 'x')

    header = OFPHeader(type = _msg_type, length = _length)
    x = UBInt8()

#class OFPECHOReply(GenericMessage):
#    _msg_type = OFPType.OFPT_ECHO_REPLY
