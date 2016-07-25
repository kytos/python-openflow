"""Defines Vendor message."""

# System imports

# Third-party imports

from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base, basic_types


__all__ = ('VendorHeader')

# Classes


class VendorHeader(base.GenericMessage):
    """OpenFlow Vendor message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = of_header.Header(message_type=of_header.Type.OFPT_VENDOR)
    vendor = basic_types.UBInt32()

    def __init__(self, xid=None, vendor=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
            vendor (int): Vendor ID:
                MSB 0: low-order bytes are IEEE OUI.
                MSB != 0: defined by OpenFlow consortium.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.vendor = vendor
