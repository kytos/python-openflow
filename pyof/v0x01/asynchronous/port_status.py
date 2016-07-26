"""Defines an Error Message."""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

__all__ = ('PortStatus', 'PortReason')

# Enums


class PortReason(enum.Enum):
    """What changed about the physical port."""

    #: The port was added
    OFPPR_ADD = 1
    #: The port was removed
    OFPPR_DELETE = 2
    #: Some attribute of the port has changed
    OFPPR_MODIFY = 3


# Classes

class PortStatus(base.GenericMessage):
    """A physical port has changed in the datapath.

    Args:
        reason (PortReason): Addition, deletion or modification.
        desc (PhyPort): Port description.
    """

    #: :class:`~.header.Header`: OpenFlow Header
    header = of_header.Header(message_type=of_header.Type.OFPT_PORT_STATUS)
    reason = basic_types.UBInt8(enum_ref=PortReason)
    #: Align to 32-bits.
    pad = basic_types.PAD(7)
    desc = phy_port.PhyPort()

    def __init__(self, xid=None, reason=None, desc=None):
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.reason = reason
        self.desc = desc
