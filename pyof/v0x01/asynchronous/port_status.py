"""Defines an Error Message."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8
# Local source tree imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import PhyPort

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

    #: :class:`~pyof.v0x01.common.header.Header`: OpenFlow Header
    header = Header(message_type=Type.OFPT_PORT_STATUS)
    reason = UBInt8(enum_ref=PortReason)
    #: Align to 32-bits.
    pad = Pad(7)
    desc = PhyPort()

    def __init__(self, xid=None, reason=None, desc=None):
        """Assign parameters to object attributes.

        Args:
            xid (int): Header's xid.
            reason (~pyof.v0x01.asynchronous.port_status.PortReason):
                Addition, deletion or modification.
            desc (PhyPort): Port description.
        """
        super().__init__(xid)
        self.reason = reason
        self.desc = desc
