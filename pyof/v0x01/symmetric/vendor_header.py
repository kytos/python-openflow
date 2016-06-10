"""Defines Vendor message"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Classes


class VendorHeader(base.GenericMessage):
    """OpenFlow Vendor message

    This message does not contain a body beyond the OpenFlow Header
        :param xid:    xid to be used on the message header
        :param vendor: Vendor ID:
                       MSB 0: low-order bytes are IEEE OUI.
                       MSB != 0: defined by OpenFlow consortium
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_ECHO_REQUEST)
    vendor = basic_types.UBInt32()

    def __init__(self, xid=None, vendor=None):
        super().__init__()
        self.header.xid = xid
        self.vendor = vendor
