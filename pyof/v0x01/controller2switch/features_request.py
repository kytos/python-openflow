"""Defines Features Request classes and related items."""

from pyof.foundation.base import GenericMessage
from pyof.v0x01.common.header import Header, Type

__all__ = ('FeaturesRequest',)

# Classes


class FeaturesRequest(GenericMessage):
    """Features request message.

    This message does not contain a body in addition to the OpenFlow Header.
    """

    header = Header(
        message_type=Type.OFPT_FEATURES_REQUEST)

    def __init__(self, xid=None):
        """The constructor takes the optional parameter below.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__(xid)
