"""Defines Vendor message."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import UBInt32
from pyof.v0x01.common.header import Header, Type

__all__ = ('VendorHeader',)

# Classes


class VendorHeader(GenericMessage):
    """OpenFlow Vendor message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header(message_type=Type.OFPT_VENDOR)
    vendor = UBInt32()

    def __init__(self, xid=None, vendor=None):
        """The constructor takes the parameters below.

        Args:
            xid (int): xid to be used on the message header.
            vendor (int): Vendor ID:
                MSB 0: low-order bytes are IEEE OUI.
                MSB != 0: defined by OpenFlow consortium.
        """
        super().__init__(xid)
        self.vendor = vendor
