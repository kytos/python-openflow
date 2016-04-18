"""Defines Vendor message"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types

# Classes


class VendorHeader(base.GenericStruct):
    """OpenFlow Vendor message

    This message does not contain a body beyond the OpenFlow Header
        :param xid -- xid to be used on the message header
        :param vendor -- Vendor ID:
                         MSB 0: low-order bytes are IEEE OUI.
                         MSB != 0: defined by OpenFlow consortium
    """
    header = of_header.OFPHeader()
    vendor = basic_types.UBInt32()

    def __init__(self, xid=None, vendor=None):
        self.header.ofp_type = of_header.OFPType.OFPT_ECHO_REQUEST
        self.header.length = 12
        self.header.xid = xid
        self.vendor = vendor
