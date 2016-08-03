"""Defines Get Config Request classes and related items."""

from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.foundation.base import GenericMessage

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
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
