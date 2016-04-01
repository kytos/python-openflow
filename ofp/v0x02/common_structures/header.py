from common.basic_types import UBInt8, UBInt16, UBInt32
from common.base import GenericStruct

class OFPHeader(GenericStruct):
    version = UBInt8()
    ofp_type = UBInt8()
    length = UBInt16()
    xid = UBInt32()



