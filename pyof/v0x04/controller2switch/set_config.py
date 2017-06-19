"""Define SetConfig message."""

# System imports

# Third-party imports

# Local imports
from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.common import SwitchConfig

__all__ = ('SetConfig',)


class SetConfig(SwitchConfig):
    """Set config message."""

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            flags (:class:`pyof.v0x01.controller2switch.common.ConfigFlags`):
                                 OFPC_* flags.
            miss_send_len (int): UBInt16 max bytes of new flow that the
                                 datapath should send to the controller.
        """
        super().__init__(xid, flags, miss_send_len)
        self.header.message_type = Type.OFPT_SET_CONFIG
