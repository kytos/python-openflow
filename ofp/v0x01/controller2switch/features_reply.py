"""Defines Features Reply classes and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from foundation import base
from foundation import basic_types
from common import header as of_header


# Enums


class Capabilities(enum.Enum):
    """Enumeration of Capabilities supported by the datapath

        OFPC_FLOW_STATS   # Flow statistics
        OFPC_TABLE_STATS  # Table statistics
        OFPC_PORT_STATS   # Port statistics
        OFPC_GROUP_STATS  # Group statistics
        OFPC_IP_REASM     # Can reassemble IP fragments
        OFPC_QUEUE_STATS  # Queue statistics
        OFPC_ARP_MATCH_IP # Match IP addresses in ARP pkts
    """
    OFPC_FLOW_STATS = 1 << 0
    OFPC_TABLE_STATS = 1 << 1   # Table statistics
    OFPC_PORT_STATS = 1 << 2    # Port statistics
    OFPC_GROUP_STATS = 1 << 3   # Group statistics
    OFPC_IP_REASM = 1 << 5      # Can reassemble IP fragments
    OFPC_QUEUE_STATS = 1 << 6   # Queue statistics
    OFPC_ARP_MATCH_IP = 1 << 7  # Match IP addresses in ARP pkts


# Classes


class SwitchFeatures(base.GenericStruct):
    """Message sent by the switch device to the controller.

    This message is the response for a features_request
    message, sent by the controller to the switch device.
    The 'OFPT_FEATURES_REPLY' message is an instance of this
    class, despite the strange name.

        :param xid:          xid to be used on the message header
        :param datapath_id:  UBInt64 datapath unique ID
                             The lower 48-bits are for MAC address, while
                             the upper 16-bits are implementer-defined
        :param n_buffers:    UBInt32 max packets buffered at once
        :param n_tables:     UBInt8 number of tables supported by datapath
        :param capabilities: UBInt32 bitmap support of capabilities
        :param reserved:     UBInt32
        :param ports:        Port definitions
    """

    header = of_header.OFPHeader()
    datapath_id = basic_types.UBInt64
    n_buffers = basic_types.UBInt32
    n_tables = basic_types.UBInt8
    pad = basic_types.UBInt8Array(length=3) # Align to 64-bits
    # Features
    capabilities = basic_types.UBInt32
    reserved = basic_types.UBInt32

    # Port info
    # TODO: On the official spec this element acts like a pointer to the first
    #       element of a list of ports. Considering that this class must have
    #       a size of 32, should we use a pointer in python? Or a list?
    #       In the case of using a pointer, should we create a class that
    #       represents a list of ports and then point to an instance of it?
    #       We should consider that in Python all objects acts as C++ pointers
    # https://rg03.wordpress.com/2007/04/21/semantics-of-python-variable-names-from-a-c-perspective/
    ports = None # The number of ports is inferred
                            # from the length field in the header

    def __init__(self,
                 xid=None,
                 datapath_id=None,
                 n_buffers=0,
                 ntables=0,
                 pad=0,
                 capabilities=0,
                 reserved=0,
                 ports=None):
        self.header.ofp_type = of_header.OFPType.OFPT_FEATURES_REPLY
        self.header.xid = xid
        self.datapath_id = datapath_id
        self.n_buffers = n_buffers
        self.ntables = ntables
        self.pad = pad
        self.capabilities = capabilities
        self.reserved = reserved
        self.ports = ports
