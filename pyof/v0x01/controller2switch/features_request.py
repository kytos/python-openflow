"""Defines Features Request classes and related items."""

from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

__all__ = ('FeaturesRequest',)

# Classes


class FeaturesRequest(base.GenericMessage):
    """Features request message.

    This message does not contain a body in addition to the OpenFlow Header.
    """

    header = of_header.Header(
        message_type=of_header.Type.OFPT_FEATURES_REQUEST)

    def __init__(self, xid=None):
        """The constructor takes the optional parameter below.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__(xid)
