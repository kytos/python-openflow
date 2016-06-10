"""Modifications to the flow table from the controller"""

# System imports
import enum
# Third-party imports

# Local source tree imports
from pyof.v0x01.common import flow_match
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


# Enums

class FlowModCommand(enum.Enum):
    """
    List the possible commands for a flow.

    Enums:
        OFPFC_ADD           # New Flow
        OFPFC_MODIFY        # Modify all flows
        OFPFC_MODIFY_STRICT # Modify entry strictly matching wildcards
        OFPFC_DELETE        # Delete all matching flows
        OFPFC_DELETE_STRICT # Strictly match wildcards and priority

    """
    OFPFC_ADD = 0
    OFPFC_MODIFY = 1
    OFPFC_MODIFY_STRICT = 2
    OFPFC_DELETE = 3
    OFPFC_DELETE_STRICT = 4


class FlowModFlags(base.GenericBitMask):
    """Types to be used in Flags field"""
    #: Send flow removed message when flow expires or is deleted
    OFPFF_SEND_FLOW_REM = 1 << 0
    #: Check for overlapping entries first
    OFPFF_CHECK_OVERLAP = 1 << 1
    #: Remark this is for emergency
    OFPFF_EMERG = 1 << 2


# Classes


class FlowMod(base.GenericMessage):
    """
    Modifies the flow table from the controller.

    :param xid:          xid to be used on the message header
    :param match:        Fields to match
    :param cookie:       Opaque controller-issued identifier
    :param command:      One of OFPFC_*
    :param idle_timeout: Idle time before discarding (seconds)
    :param hard_timeout: Max time before discarding (seconds)
    :param priority:     Priority level of flow entry
    :param buffer_idle:  Buffered packet to apply to (or -1).
                         Not meaningful for OFPFC_DELETE*
    :param out_port:     For OFPFC_DELETE* commands, require matching
                         entries to include this as an output port.
                         A value of OFPP_NONE indicates no restriction.
    :param flags:        One of OFPFF_*
    :param actions:      The action length is inferred from the length
                         field in the header
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_FLOW_MOD)
    match = flow_match.Match()
    cookie = basic_types.UBInt64()
    command = basic_types.UBInt16(enum_ref=FlowModCommand)
    idle_timeout = basic_types.UBInt16()
    hard_timeout = basic_types.UBInt16()
    priority = basic_types.UBInt16()
    buffer_id = basic_types.UBInt32()
    out_port = basic_types.UBInt16(enum_ref=phy_port.Port)
    flags = basic_types.UBInt16(enum_ref=FlowModFlags)
    actions = common.ListOfActions()

    def __init__(self, xid=None, match=None, cookie=None, command=None,
                 idle_timeout=None, hard_timeout=None, priority=None,
                 buffer_id=None, out_port=None, flags=None, actions=None):
        super().__init__()
        self.header.xid = xid
        self.match = match
        self.cookie = cookie
        self.command = command
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.priority = priority
        self.buffer_id = buffer_id
        self.out_port = out_port
        self.flags = flags
        self.actions = [] if actions is None else actions
