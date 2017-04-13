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
