"""Modifications to the flow table from the controller."""

# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8, UBInt16, UBInt32, UBInt64
from pyof.v0x04.common.constants import OFP_NO_BUFFER
from pyof.v0x04.common.flow_instructions import ListOfInstruction
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.group_mod import Group

__all__ = ('FlowMod', 'FlowModCommand', 'FlowModFlags')

# Enums


class FlowModCommand(IntEnum):
    """List the possible commands for a flow."""

    #: New flow
    OFPFC_ADD = 0
    #: Modify all matching flows
    OFPFC_MODIFY = 1
    #: Modify entry strictly matching wildcards and priority.
    OFPFC_MODIFY_STRICT = 2
    #: Delete all matching flows
    OFPFC_DELETE = 3
    #: Strictly match wildcards and priority
    OFPFC_DELETE_STRICT = 4


class FlowModFlags(GenericBitMask):
    """Types to be used in Flags field."""

    #: Send flow removed message when flow expires or is deleted
    OFPFF_SEND_FLOW_REM = 1 << 0
    #: Check for overlapping entries first.
    OFPFF_CHECK_OVERLAP = 1 << 1
    #: Reset flow packet and byte counts.
    OFPFF_RESET_COUNTS = 1 << 2
    #: Don’t keep track of packet count.
    OFPFF_NO_PKT_COUNTS = 1 << 3
    #: Don’t keep track of byte count.
    OFPFF_NO_BYT_COUNTS = 1 << 4


# Classes
class FlowMod(GenericMessage):
    """Modifies the flow table from the controller."""

    header = Header(message_type=Type.OFPT_FLOW_MOD)
    cookie = UBInt64()
    cookie_mask = UBInt64()

    # Flow actions
    table_id = UBInt8()
    command = UBInt8(enum_ref=FlowModCommand)
    idle_timeout = UBInt16()
    hard_timeout = UBInt16()
    priority = UBInt16()
    buffer_id = UBInt32()
    out_port = UBInt32()
    out_group = UBInt32()
    flags = UBInt16(enum_ref=FlowModFlags)
    pad = Pad(2)
    match = Match()
    instructions = ListOfInstruction()

    def __init__(self, xid=None, cookie=0, cookie_mask=0, table_id=0,
                 command=None, idle_timeout=0, hard_timeout=0,
                 priority=0, buffer_id=OFP_NO_BUFFER, out_port=PortNo.OFPP_ANY,
                 out_group=Group.OFPG_ANY,
                 flags=FlowModFlags.OFPFF_SEND_FLOW_REM,
                 match=None, instructions=None):
        """Create a FlowMod with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            cookie (int): Opaque controller-issued identifier.
            cookie_mask (int): Mask used to restrict the cookie bits that must
                match when the command is OFPFC_MODIFY* or OFPFC_DELETE*. A
                value of 0 indicates no restriction.
            table_id (int): ID of the table to put the flow in. For
                OFPFC_DELETE_* commands, OFPTT_ALL can also be used to delete
                matching flows from all tables.
            command (~pyof.v0x04.controller2switch.flow_mod.FlowModCommand):
                One of OFPFC_*.
            idle_timeout (int): Idle time before discarding (seconds).
            hard_timeout (int): Max time before discarding (seconds).
            priority (int): Priority level of flow entry.
            buffer_id (int): Buffered packet to apply to, or OFP_NO_BUFFER. Not
                meaningful for OFPFC_DELETE*.
            out_port (int): For OFPFC_DELETE* commands, require matching
                entries to include this as an output port. A value of OFPP_ANY
                indicates no restriction.
            out_group (int): For OFPFC_DELETE* commands, require matching
                entries to include this as an output group. A value of OFPG_ANY
                indicates no restriction.
            flags (~pyof.v0x04.controller2switch.flow_mod.FlowModFlags):
                One of OFPFF_*.
            match (~pyof.v0x04.common.flow_match.Match):
                Fields to match. Variable size.
        """
        super().__init__(xid)
        self.cookie = cookie
        self.cookie_mask = cookie_mask
        self.table_id = table_id
        self.command = command
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.priority = priority
        self.buffer_id = buffer_id
        self.out_port = out_port
        self.out_group = out_group
        self.flags = flags
        self.match = Match() if match is None else match
        self.instructions = instructions or ListOfInstruction()
