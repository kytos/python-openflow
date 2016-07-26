"""Modifications to the flow table from the controller."""

# System imports
import enum

from pyof.v0x01.common import header as of_header
# Local source tree imports
from pyof.v0x01.common import flow_match, phy_port
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base, basic_types


# Third-party imports

__all__ = ('FlowMod', 'FlowModCommand', 'FlowModFlags')

# Enums


class FlowModCommand(enum.Enum):
    """List the possible commands for a flow."""

    #: New flow
    OFPFC_ADD = 0
    #: Modify all flows
    OFPFC_MODIFY = 1
    #: Modify entry strictly matching wildcards
    OFPFC_MODIFY_STRICT = 2
    #: Delete all matching flows
    OFPFC_DELETE = 3
    #: Strictly match wildcards and priority
    OFPFC_DELETE_STRICT = 4


class FlowModFlags(base.GenericBitMask):
    """Types to be used in Flags field."""

    #: Send flow removed message when flow expires or is deleted
    OFPFF_SEND_FLOW_REM = 1 << 0
    #: Check for overlapping entries first
    OFPFF_CHECK_OVERLAP = 1 << 1
    #: Remark this is for emergency
    OFPFF_EMERG = 1 << 2


# Classes


class FlowMod(base.GenericMessage):
    """Modifies the flow table from the controller."""

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
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            match (Match): Fields to match.
            cookie (int): Opaque controller-issued identifier.
            command (FlowModCommand): One of OFPFC_*.
            idle_timeout (int): Idle time before discarding (seconds).
            hard_timeout (int): Max time before discarding (seconds).
            priority (int): Priority level of flow entry.
            buffer_idle (int): Buffered packet to apply to (or -1).
                Not meaningful for OFPFC_DELETE*.
            out_port (Port): For OFPFC_DELETE* commands, require matching
                entries to include this as an output port.
                A value of OFPP_NONE indicates no restriction.
            flags (FlowModFlags): One of OFPFF_*.
            actions (ListOfActions): The action length is inferred from the
                length field in the header.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
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
