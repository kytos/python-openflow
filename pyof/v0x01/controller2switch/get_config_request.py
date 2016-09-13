"""Defines Get Config Request classes and related items."""

from pyof.foundation.base import GenericMessage
from pyof.v0x01.common.header import Header, Type

__all__ = ('GetConfigRequest',)

# Classe


class GetConfigRequest(GenericMessage):
    """Get Config Request message."""

    header = Header(message_type=Type.OFPT_GET_CONFIG_REQUEST)

    def __init__(self, xid=None):
        """The constructor just assings parameters to object attributes.

        This message does not contain a body beyond the OpenFlow Header.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__(xid)
