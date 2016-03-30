from ofp.v0x02.basic_types import UBInt8, UBInt16, UBInt32
from ofp.v0x02.common.generic import GenericStruct

class OFPHeader(GenericStruct):
    version = UBInt8()
    ofp_type = UBInt8()
    length = UBInt16()
    xid = UBInt32()



