"""Helper python-openflow functions"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common.header import Type

# Importing asynchronous messages
from pyof.v0x01.asynchronous.error_msg import ErrorMsg
from pyof.v0x01.asynchronous.flow_removed import FlowRemoved
from pyof.v0x01.asynchronous.packet_in import PacketIn
from pyof.v0x01.asynchronous.port_status import PortStatus

# Importing controller2switch messages
from pyof.v0x01.controller2switch.barrier_reply import BarrierReply
from pyof.v0x01.controller2switch.barrier_request import BarrierRequest
from pyof.v0x01.controller2switch.features_reply import FeaturesReply
from pyof.v0x01.controller2switch.features_request import FeaturesRequest
from pyof.v0x01.controller2switch.flow_mod import FlowMod
from pyof.v0x01.controller2switch.get_config_reply import GetConfigReply
from pyof.v0x01.controller2switch.get_config_request import GetConfigRequest
from pyof.v0x01.controller2switch.packet_out import PacketOut
from pyof.v0x01.controller2switch.port_mod import PortMod
from pyof.v0x01.controller2switch.queue_get_config_reply import QueueGetConfigReply
from pyof.v0x01.controller2switch.queue_get_config_request import QueueGetConfigRequest
from pyof.v0x01.controller2switch.set_config import SetConfig
from pyof.v0x01.controller2switch.stats_reply import StatsReply
from pyof.v0x01.controller2switch.stats_request import StatsRequest

# Importing symmetric messages
from pyof.v0x01.symmetric.echo_reply import EchoReply
from pyof.v0x01.symmetric.hello import Hello
from pyof.v0x01.symmetric.vendor_header import VendorHeader
from pyof.v0x01.symmetric.echo_request import EchoRequest


__all__ = ['new_message_from_header', 'new_message_from_message_type']


def new_message_from_message_type(message_type):
    """Method that receives an OpenFlow Message Type and then returns an
    empty message of that type.

    Args:
        messageType (Type): python-openflow message :class:~.common.header.Type

    Returns:
        empty OpenFlow message of the requested message type

    Raises:
        KytosUndefinedMessageType: unkown Message_Type
    """
    if not isinstance(message_type, Type):
        raise ValueError

    available_classes = {
        Type.OFPT_HELLO: Hello,
        Type.OFPT_ERROR: ErrorMsg,
        Type.OFPT_ECHO_REQUEST: EchoRequest,
        Type.OFPT_ECHO_REPLY: EchoReply,
        Type.OFPT_VENDOR: VendorHeader,
        Type.OFPT_FEATURES_REQUEST: FeaturesRequest,
        Type.OFPT_FEATURES_REPLY: FeaturesReply,
        Type.OFPT_GET_CONFIG_REQUEST: GetConfigRequest,
        Type.OFPT_GET_CONFIG_REPLY: GetConfigReply,
        Type.OFPT_SET_CONFIG: SetConfig,
        Type.OFPT_PACKET_IN: PacketIn,
        Type.OFPT_FLOW_REMOVED: FlowRemoved,
        Type.OFPT_PORT_STATUS: PortStatus,
        Type.OFPT_PACKET_OUT: PacketOut,
        Type.OFPT_FLOW_MOD: FlowMod,
        Type.OFPT_PORT_MOD: PortMod,
        Type.OFPT_STATS_REQUEST: StatsRequest,
        Type.OFPT_STATS_REPLY: StatsReply,
        Type.OFPT_BARRIER_REQUEST: BarrierRequest,
        Type.OFPT_BARRIER_REPLY: BarrierReply,
        Type.OFPT_QUEUE_GET_CONFIG_REQUEST: QueueGetConfigRequest,
        Type.OFPT_QUEUE_GET_CONFIG_REPLY: QueueGetConfigReply
    }

    message_class = available_classes.get(message_type)
    message_instance = message_class()

    return message_instance


def new_message_from_header(header):
    """Method that receives a OpenFlowHeader and then returns an empty message
    regarding the message_type attribute from the header.

    Args:
        header (Header): Unpacked OpenFlow Header

    Returns:
        empty OpenFlow message of the same type of message_type attribute from
        the given header. The header attribute of the message will be populated

    Raises:
        KytosUndefinedMessageType: unkown Message_Type
    """
    message_type = header.message_type
    if not isinstance(message_type, Type):
        try:
            if isinstance(message_type, str):
                message_type = Type[message_type]
            elif isinstance(message_type, int):
                message_type = Type(message_type)
        except ValueError:
            raise ValueError

    message = new_message_from_message_type(message_type)
    message.header.xid = header.xid
    message.header.length = header.length

    return message
