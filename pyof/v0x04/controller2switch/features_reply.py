"""Defines Features Reply classes and related items."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericMessage
from pyof.foundation.basic_types import Pad, UBInt8, UBInt32, UBInt64
from pyof.v0x04.common.header import Header, Type

__all__ = ('FeaturesReply', 'Capabilities', 'SwitchFeatures')


class Capabilities(GenericBitMask):
    """Capabilities supported by the datapath."""

    #: Flow statistics
    OFPC_FLOW_STATS = 1 << 0
    #: Table statistics
    OFPC_TABLE_STATS = 1 << 1
    #: Port statistics
    OFPC_PORT_STATS = 1 << 2
    #: Group statistics.
    OFPC_GROUP_STATS = 1 << 3
    #: Can reassembe IP fragments
    OFPC_IP_REASM = 1 << 5
    #: Queue statistics
    OFPC_QUEUE_STATS = 1 << 6
    #: Switch will block looping ports.
    OFPC_PORT_BLOCKED = 1 << 8


# Classes

class SwitchFeatures(GenericMessage):
    """Message sent by the switch device to the controller.

    This message is the response for a features_request message, sent by the
    controller to the switch device. The 'OFPT_FEATURES_REPLY' message inherits
    from this class, despite the strange name.
    """

    header = Header(message_type=Type.OFPT_FEATURES_REPLY)
    datapath_id = UBInt64()

    n_buffers = UBInt32()

    n_tables = UBInt8()
    auxiliary_id = UBInt8()
    #: Align to 64-bits.
    pad = Pad(2)

    # Features
    capabilities = UBInt32(enum_ref=Capabilities)
    reserved = UBInt32()

    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 n_tables=None, auxiliary_id=None, capabilities=None,
                 reserved=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            datapath_id (int): Datapath unique ID.
                The lower 48-bits are for MAC address, while
                the upper 16-bits are implementer-defined.
            n_buffers (int): Max packets buffered at once.
            n_tables (int): Number of tables supported by datapath.
            auxiliary_id (int): Identify auxiliary connections.
            capabilities (int): bitmap of supported capabilities.
            reserved (int): Reserved.
        """
        super().__init__(xid)
        self.datapath_id = datapath_id
        self.n_buffers = n_buffers
        self.n_tables = n_tables
        self.auxiliary_id = auxiliary_id
        self.capabilities = capabilities
        self.reserved = reserved


class FeaturesReply(SwitchFeatures):
    """'OFPT_FEATURES_REPLY' message."""
