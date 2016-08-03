"""Defines Get Config Request classes and related items."""

from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

__all__ = ('GetConfigRequest',)

# Classe


class GetConfigRequest(base.GenericMessage):
    """Get Config Request message."""

    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REQUEST)

    def __init__(self, xid=None):
        """The constructor just assings parameters to object attributes.

        This message does not contain a body beyond the OpenFlow Header.

        Args:
            xid (int): xid to be used on the message header.
        """
        super().__init__(xid)
