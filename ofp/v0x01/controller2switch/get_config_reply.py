"""Defines Features Reply classes and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from common import header as of_header
from foundation import base
from foundation import basic_types


# Enums


class ConfigFlags(enum.Enum):
    """Configuratin Flags

        # Handling of IP Fragments
        OFPC_FRAG_NORMAL               # No special handling for fragments
        OFPC_FRAG_DROP                 # Drop fragments
        OFPC_FRAG_REASM                # Reassemble (only if OFPC_IP_REASM set)
        OFPC_FRAG_MASK

        # TTL processing - applicable for IP and MPLS packets
        OFPC_INVALID_TTL_TO_CONTROLLER # Send packets with invalid TTL
                                       # i.e. 0 or 1 to controller
    """
    OFPC_FRAG_NORMAL = 0
    OFPC_FRAG_DROP = 1 << 0
    OFPC_FRAG_REASM = 1 << 1
    OFPC_FRAG_MASK = 3
    OFPC_INVALID_TTL_TO_CONTROLLER = 1 << 2


# Classes


class SwitchConfig(base.GenericStruct):
    """Message used on OFPT_SET_CONFIG and OFPT_GET_CONFIG_REPLY.

    This is OFPT_GET_CONFIG_REPLY message sent by the switch to
    the controller in response to the OFPT_GET_CONFIG_REQUEST,
    and also is the OFPT_SET_CONFIG message sent by the controller
    to the switch.

        :param xid:           xid to be used on the message header
        :param set_message:   Boolean to define if the message is
                              a SET_CONFIG or GET_CONFIG_REPLY.
                              - True (default): OFPT_SET_CONFIG
                              - False: OFPT_GET_CONFIG_REPLY
        :param flags:         UBInt16 OFPC_* flags
        :param miss_send_len: UBInt16 max bytes of new flow that the
                              datapath should send to the controller
    """

    header = of_header.OFPHeader()
    flags = basic_types.UBInt16
    miss_send_len = basic_types.UBInt16

    def __init__(self, xid=None, set_message=True, flags=None,
                 miss_send_len=None):

        if set_message:
            self.header.ofp_type = of_header.OFPType.OFPT_SET_CONFIG
        else:
            self.header.ofp_type = of_header.OFPType.OFPT_GET_CONFIG_REPLY
        self.header.xid = xid
        self.flags = flags
        self.miss_send_len = miss_send_len
