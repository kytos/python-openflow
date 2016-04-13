"""Defines Features Reply classes and related items"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from ..common import header as of_header
from ..common import port
from ..foundation import base
from ..foundation import basic_types


# Enums


class Capabilities(enum.Enum):
    """Enumeration of Capabilities supported by the datapath

    Enums:
        OFPC_FLOW_STATS     # Flow statistics
        OFPC_TABLE_STATS    # Table statistics
        OFPC_PORT_STATS     # Port statistics
        OFPC_STP            # 802.1d spanning tree
        OFPC_RESERVED       # Reserved, must be zero
        OFPC_IP_REASM       # Can reassembe IP fragments
        OFPC_QUEUE_STATS    # Queue statistics
        OFPC_ARP_MATCH_IP   # Match IP addresses in ARP pkts
    """
    OFPC_FLOW_STATS = 1 << 0
    OFPC_TABLE_STATS = 1 << 1
    OFPC_PORT_STATS = 1 << 2
    OFPC_STP = 1 << 3
    OFPC_RESERVED = 1 << 4
    OFPC_IP_REASM = 1 << 5
    OFPC_QUEUE_STATS = 1 << 6
    OFPC_ARP_MATCH_IP = 1 << 7


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
        :param ports:        Port definitions
    """

    header = of_header.OFPHeader()
    datapath_id = basic_types.UBInt64()
    n_buffers = basic_types.UBInt32()
    n_tables = basic_types.UBInt8()
    pad = basic_types.UBInt8Array(length=3)  # Align to 64-bits
    # Features
    capabilities = basic_types.UBInt32()
    actions = basic_types.UBInt32()

    # Port info
    # TODO: On the official spec this element acts like a pointer to the first
    #       element of a list of ports. Considering that this class must have
    #       a size of 32, should we use a pointer in python? Or a list?
    #       In the case of using a pointer, should we create a class that
    #       represents a list of ports and then point to an instance of it?
    #       We should consider that in Python all objects acts as C++ pointers
    #       https://goo.gl/p1nzxh
    # The number of ports is inferred from the length field in the header
    ports = port.Port()

    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 ntables=None, pad=None, capabilities=None, ports=None):

        self.header.ofp_type = of_header.OFPType.OFPT_FEATURES_REPLY
        self.header.xid = xid
        self.datapath_id = datapath_id
        self.n_buffers = n_buffers
        self.ntables = ntables
        self.pad = pad
        self.capabilities = capabilities
        self.ports = ports
