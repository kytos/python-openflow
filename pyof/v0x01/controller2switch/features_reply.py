"""Defines Features Reply classes and related items"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class Capabilities(base.GenericBitMask):
    """Capabilities supported by the datapath

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

class SwitchFeatures(base.GenericMessage):
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
    :param capabilities: UBInt32 bitmap of supported capabilities
    :param actions:      UBInt32 Bitmap of supported "action_type"s
    :param ports:        Port definitions
    """
    header = of_header.Header(message_type=of_header.Type.OFPT_FEATURES_REPLY)
    datapath_id = basic_types.UBInt64()
    n_buffers = basic_types.UBInt32()
    n_tables = basic_types.UBInt8()
    pad = basic_types.PAD(3)  # Align to 64-bits
    # Features
    capabilities = basic_types.UBInt32(enum_ref=Capabilities)
    actions = basic_types.UBInt32()
    ports = phy_port.ListOfPhyPorts()

    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 n_tables=None, capabilities=None, actions=None, ports=None):
        super().__init__()
        self.header.xid = xid
        self.datapath_id = datapath_id
        self.n_buffers = n_buffers
        self.n_tables = n_tables
        self.capabilities = capabilities
        self.actions = actions
        self.ports = [] if ports is None else ports


class FeaturesReply(SwitchFeatures):
    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 n_tables=None, capabilities=None, actions=None, ports=None):
        self.__ordered__ = super().__ordered__  # pylint: disable=no-member
        super().__init__(xid, datapath_id, n_buffers, n_tables, capabilities,
                         actions, ports)
