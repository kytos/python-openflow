from ofp.v0x01.types import UBInt8, UBInt16, UBInt32, Char
from ofp.v0x01.exceptions import OFPException
from ofp.v0x01.conts import OFP_MAX_PORT_NAME_LEN

class GenericStruct():
    def __init__(self, **kwargs):
        self.pack_order = None
        for a in kwargs:
            try:
                field = getattr(self, a)
                field.value = kwargs[a]
            except AttributeError:
                raise OFPException("Attribute error: %s" % a)

    def build(self):
        hexa = "" 
        for field in self._build_order:
            hexa += getattr(self, field).build()
        return hexa

    def parse(self, buff):
        begin = 0
        for field in self._build_order:
            size = getattr(self, field).get_size()
            getattr(self,field).parse(buff, offset=begin)
            begin += size

class OFPHeader(GenericStruct):
    # TODO: Remove _build_order attribute. To do that, we need
    # figure out how get attributes in defined order.
    _build_order=('version', 'type', 'length', 'xid')

    # Attributes
    version = UBInt8()  # OFP_VERSION
    type = UBInt8()     # One of the OFPType
    length = UBInt16()  # Length including this ofp_header.
    xid = UBInt32()     # Transaction id associated with this packet.
                        # Replies use the same id as was in the request
                        # to facilitate pairing.
