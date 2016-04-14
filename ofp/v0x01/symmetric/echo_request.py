"""Defines Echo Request message during the handshake"""

# System imports

# Third-party imports

# Local source tree imports
from ..common import header as of_header
from ..foundation import base


class OFPRequest(base.GenericStruct):
    """OpenFlow Reply message

    This message does not contain a body beyond the OpenFlow Header
        :param xid: xid to be used on the message header
    """
    header = of_header.OFPHeader()

    def __init__(self, xid=None):
        self.header.ofp_type = of_header.OFPType.OFPT_ECHO_REQUEST
        self.header.xid = xid
