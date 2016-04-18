"""Defines Hello message"""

# System imports

# Third-party imports

# Local source tree imports
from ..common import header as of_header
from ..foundation import base


class OFPHello(base.GenericStruct):
    """OpenFlow Hello Message

    This message does not contain a body beyond the OpenFlow Header
        :param length: length of the message
        :param xid: xid to be used on the message header
    """
    header = of_header.OFPHeader()

    def __init__(self, length=8, xid=None):
        self.header.ofp_type = of_header.OFPType.OFPT_HELLO
        self.header.length = length
        self.header.xid = xid
