"""Define SetConfig message."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common

__all__ = ('SetConfig')


class SetConfig(common.SwitchConfig):
    """Set config message.

    Args:
        xid (int): xid to be used on the message header.
        flags (ConfigFlags): OFPC_* flags.
        miss_send_len (int): UBInt16 max bytes of new flow that the datapath
            should send to the controller.
    """

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        self.__ordered__ = super().__ordered__  # pylint: disable=no-member
        super().__init__(xid, flags, miss_send_len)
        self.header.message_type = of_header.Type.OFPT_SET_CONFIG
