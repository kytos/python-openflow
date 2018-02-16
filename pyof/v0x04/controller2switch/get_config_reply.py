"""Defines Get Config Reply message."""

# System imports

# Third-party imports

from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.common import SwitchConfig

__all__ = ('GetConfigReply',)


class GetConfigReply(SwitchConfig):
    """Get Config Reply message."""

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        """Create a GetConfigReply with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            flags (~pyof.v0x04.controller2switch.common.ConfigFlag):
                OFPC_* flags.
            miss_send_len (int): UBInt16 max bytes of new flow that the
                datapath should send to the controller.
        """
        super().__init__(xid, flags, miss_send_len)
        self.header.message_type = Type.OFPT_GET_CONFIG_REPLY
