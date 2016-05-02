"""Modifications to the flow table from the controller"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import flow_match
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


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
    OFPFC_ADD = 1
    OFPFC_MODIFY = 2
    OFPFC_MODIFY_STRICT = 3
    OFPFC_DELETE = 4
    OFPFC_DELETE_STRICT = 5


class FlowModFlags(enum.Enum):
    """
    Types to be used in Flags field

    Enums:
        OFPFF_SEND_FLOW_REM # Send flow removed message when flow
                              expires or is deleted
        OFPFF_CHECK_OVERLAP # Check for overlapping entries first
        OFPFF_EMERG         # Remark this is for emergency
    """
    OFPFF_SEND_FLOW_REM = 1 << 0
    OFPFF_CHECK_OVERLAP = 1 << 1
    OFPFF_EMERG = 1 << 2


# Classes


class FlowMod(base.GenericStruct):
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
    header = of_header.OFPHeader()
    match = flow_match.OFPMatch()
    cookie = basic_types.UBInt64()
    command = basic_types.UBInt16()
    idle_timeout = basic_types.UBInt16()
    hard_timeout = basic_types.UBInt16()
    priority = basic_types.UBInt16()
    buffer_id = basic_types.UBInt32()
    out_port = basic_types.UBInt16()
    flags = basic_types.UBInt16()
    actions = []
    # TODO: Add here a new type, list of ActionHeaders()
    # objects. Related to ISSUE #3

    def __init__(self, xid=None, match=None, cookie=None, command=None,
                 idle_timeout=None, hard_timeout=None, priority=None,
                 buffer_id=None, out_port=None, flags=None, actions=None):
        self.header.ofp_type = of_header.OFPType.OFPT_FLOW_MOD
        self.header.length = 0
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
        self.actions = actions
