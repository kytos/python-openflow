"""Defines common structures and enums for controller2switch"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


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


class SwitchConfig(base.GenericStruct):
    """Message used on OFPT_SET_CONFIG and OFPT_GET_CONFIG_REPLY.

    This is OFPT_GET_CONFIG_REPLY message sent by the switch to
    the controller in response to the OFPT_GET_CONFIG_REQUEST,
    and also is the OFPT_SET_CONFIG message sent by the controller
    to the switch.

        :param xid:           xid to be used on the message header
        :param flags:         UBInt16 OFPC_* flags
        :param miss_send_len: UBInt16 max bytes of new flow that the
                              datapath should send to the controller
    """

    header = of_header.Header()
    flags = basic_types.UBInt16()
    miss_send_len = basic_types.UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):

        self.header.xid = xid
        self.flags = flags
        self.miss_send_len = miss_send_len
