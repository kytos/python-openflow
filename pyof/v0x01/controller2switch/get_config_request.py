"""Defines Get Config Request classes and related items"""

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base

# Classe


class GetConfigRequest(base.GenericMessage):
    """Get Config Request message.

    This message does not contain a body beyond the OpenFlow Header
        :param xid: xid to be used on the message header
    """
    header = of_header.Header(
        message_type=of_header.Type.OFPT_GET_CONFIG_REQUEST)

    def __init__(self, xid=None):
        super().__init__()
        self.header.xid = xid
