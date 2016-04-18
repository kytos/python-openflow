"""Defines an Error Message"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ..common import header as of_header
from ..common import port
from ..foundation import base
from ..foundation import basic_types

# Enums

class PortReason(enum.Enum):
    """
    What changed about the physical port

    Enums:
        OFPPR_ADD       # The port was added
        OFPPR_DELETE    # The port was removed
        OFPPR_MODIFY    # Some attribute of the port has changed

    """
    OFPPR_ADD = 1
    OFPPR_DELETE = 2
    OFPPR_MODIFY = 3


class PortStatus(base.GenericStruct):
    """
    A physical port has changed in the datapath

        :param header -- Openflow Header
        :param reason -- One of OFPPR_*
        :param pad -- Align to 32-bits
        :param desc -- Port description

    """
    header = of_header.OFPHeader()
    reason = basic_types.UBInt8()
    pad = basic_types.UBInt8Array(length=7)
    desc = port.Port()

    def __init__(self, reason=None, pad=None, desc=None):

        self.header.ofp_type = of_header.OFPType.OFPT_PORT_STATUS
        self.reason = reason
        self.desc = desc
