"""Defines common structures and enums for controller2switch"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import action
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


# Enums


class ConfigFlags(enum.Enum):
    """Configuration Flags

        # Handling of IP Fragments
        OFPC_FRAG_NORMAL         # No special handling for fragments
        OFPC_FRAG_DROP           # Drop fragments
        OFPC_FRAG_REASM          # Reassemble (only if OFPC_IP_REASM set)
        OFPC_FRAG_MASK
    """
    OFPC_FRAG_NORMAL = 0
    OFPC_FRAG_DROP = 1
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


# Classes


class SwitchConfig(base.GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages.

    :param xid:           xid to be used on the message header
    :param flags:         UBInt16 OFPC_* flags
    :param miss_send_len: UBInt16 max bytes of new flow that the
                          datapath should send to the controller

    """

    header = of_header.Header()
    flags = basic_types.UBInt16()
    miss_send_len = basic_types.UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        super().__init__()
        self.header.xid = xid
        self.flags = flags
        self.miss_send_len = miss_send_len


class ListOfActions(basic_types.FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and
    used on ActionHeader objects

    Attributes:
        items (optional): Instance or a list of instances of ActionHeader
    """
    def __init__(self, items=None):
        super().__init__(self, pyof_class=action.ActionHeader, items=items)
