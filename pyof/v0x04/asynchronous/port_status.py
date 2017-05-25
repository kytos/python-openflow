"""Defines an PortStatus Message."""
# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import Port

# Third-party imports

__all__ = ('PortStatus', 'PortReason')

# Enums


class PortReason(IntEnum):
    """What changed about the physical port."""

    #: The port was added
    OFPPR_ADD = 0
    #: The port was removed
    OFPPR_DELETE = 1
    #: Some attribute of the port has changed
    OFPPR_MODIFY = 2


# Classes

class PortStatus(GenericMessage):
    """A physical port has changed in the datapath."""

    #: :class:`~pyof.v0x04.common.action.ActionHeader`: OpenFlow Header
    header = Header(message_type=Type.OFPT_PORT_STATUS)
    #: One of OFPPR_*.
    reason = UBInt8(enum_ref=PortReason)
    #: Align to 32-bits.
    pad = Pad(7)
    #: :class:`~pyof.v0x04.common.port.Port`
    desc = Port()

    def __init__(self, xid=None, reason=None, desc=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): Header's xid.
            reason (~pyof.v0x04.asynchronous.port_status.PortReason):
                Addition, deletion or modification.
            desc (~pyof.v0x04.common.port.Port): Port description.
        """
        super().__init__(xid)
        self.reason = reason
        self.desc = desc
