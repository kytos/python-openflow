"""Modifications to the flow table from the controller."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericBitMask, GenericMessage
from pyof.foundation.basic_types import UBInt16, UBInt32, UBInt64
from pyof.v0x01.common.action import ListOfActions
from pyof.v0x01.common.constants import NO_BUFFER
# Local source tree imports
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import Port

# Third-party imports

__all__ = ('FlowMod', 'FlowModCommand', 'FlowModFlags')

# Enums


class FlowModCommand(IntEnum):
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


class FlowModFlags(GenericBitMask):
    """Types to be used in Flags field."""

    #: Send flow removed message when flow expires or is deleted
    OFPFF_SEND_FLOW_REM = 1 << 0
    #: Check for overlapping entries first
    OFPFF_CHECK_OVERLAP = 1 << 1
    #: Remark this is for emergency
    OFPFF_EMERG = 1 << 2


# Classes
class FlowMod(GenericMessage):
    """Modifies the flow table from the controller."""

    header = Header(message_type=Type.OFPT_FLOW_MOD)
    match = Match()
    cookie = UBInt64()
    command = UBInt16(enum_ref=FlowModCommand)
    idle_timeout = UBInt16()
    hard_timeout = UBInt16()
    priority = UBInt16()
    buffer_id = UBInt32()
    out_port = UBInt16(enum_ref=Port)
    flags = UBInt16(enum_ref=FlowModFlags)
    actions = ListOfActions()

    def __init__(self, xid=None, match=None, cookie=0, command=None,
                 idle_timeout=0, hard_timeout=0, priority=0,
                 buffer_id=NO_BUFFER, out_port=Port.OFPP_NONE,
                 flags=FlowModFlags.OFPFF_SEND_FLOW_REM, actions=None):
        """Create a FlowMod with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            match (~pyof.v0x01.common.flow_match.Match): Fields to match.
            cookie (int): Opaque controller-issued identifier.
            command (~pyof.v0x01.controller2switch.flow_mod.FlowModCommand):
                One of OFPFC_*.
            idle_timeout (int): Idle time before discarding (seconds).
            hard_timeout (int): Max time before discarding (seconds).
            priority (int): Priority level of flow entry.
            buffer_idle (int): Buffered packet to apply to (or -1).
                Not meaningful for OFPFC_DELETE*.
            out_port (~pyof.v0x01.common.phy_port.Port):
                For OFPFC_DELETE* commands, require matching entries to include
                this as an output port. A value of OFPP_NONE indicates no
                restriction.
            flags (~pyof.v0x01.controller2switch.flow_mod.FlowModFlags):
                One of OFPFF_*.
            actions (~pyof.v0x01.common.action.ListOfActions):
                The action length is inferred from the length field in the
                header.
        """
        super().__init__(xid)
        self.match = match or Match()
        self.cookie = cookie
        self.command = command
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.priority = priority
        self.buffer_id = buffer_id
        self.out_port = out_port
        self.flags = flags
        self.actions = actions or []
