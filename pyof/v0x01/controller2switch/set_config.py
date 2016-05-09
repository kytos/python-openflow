"""Defines SetConfig message"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common


class SetConfig(common.SwitchConfig):

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        common.SwitchConfig.__init__(self, xid, flags, miss_send_len)
        self.header.message_type = of_header.Type.OFPT_SET_CONFIG
