"""Defines Hello message"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base

# Classes


class Hello(base.GenericStruct):
    """OpenFlow Hello Message

    This message does not contain a body beyond the OpenFlow Header
        :param length: length of the message
        :param xid:    xid to be used on the message header
    """
    header = of_header.Header()

    def __init__(self, xid=None):
        self.header.ofp_type = of_header.Type.OFPT_HELLO
        self.header.length = 8
        self.header.xid = xid
