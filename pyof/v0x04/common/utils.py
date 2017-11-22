"""Helper python-openflow functions."""

# System imports

# Third-party imports

# Local source tree imports
# Importing asynchronous messages
from pyof.v0x04.asynchronous.error_msg import ErrorMsg
from pyof.v0x04.asynchronous.flow_removed import FlowRemoved
from pyof.v0x04.asynchronous.packet_in import PacketIn
from pyof.v0x04.asynchronous.port_status import PortStatus
# Importing controller2switch messages
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.controller2switch.barrier_reply import BarrierReply
from pyof.v0x04.controller2switch.barrier_request import BarrierRequest
from pyof.v0x04.controller2switch.features_reply import FeaturesReply
from pyof.v0x04.controller2switch.features_request import FeaturesRequest
from pyof.v0x04.controller2switch.flow_mod import FlowMod
from pyof.v0x04.controller2switch.get_async_reply import GetAsyncReply
from pyof.v0x04.controller2switch.get_async_request import GetAsyncRequest
from pyof.v0x04.controller2switch.get_config_reply import GetConfigReply
from pyof.v0x04.controller2switch.get_config_request import GetConfigRequest
from pyof.v0x04.controller2switch.group_mod import GroupMod
from pyof.v0x04.controller2switch.meter_mod import MeterMod
from pyof.v0x04.controller2switch.multipart_reply import MultipartReply
from pyof.v0x04.controller2switch.multipart_request import MultipartRequest
from pyof.v0x04.controller2switch.packet_out import PacketOut
from pyof.v0x04.controller2switch.port_mod import PortMod
from pyof.v0x04.controller2switch.queue_get_config_reply import (
    QueueGetConfigReply)
from pyof.v0x04.controller2switch.queue_get_config_request import (
    QueueGetConfigRequest)
from pyof.v0x04.controller2switch.role_reply import RoleReply
from pyof.v0x04.controller2switch.role_request import RoleRequest
from pyof.v0x04.controller2switch.set_async import SetAsync
from pyof.v0x04.controller2switch.set_config import SetConfig
from pyof.v0x04.controller2switch.table_mod import TableMod
# Importing symmetric messages
from pyof.v0x04.symmetric.echo_reply import EchoReply
from pyof.v0x04.symmetric.echo_request import EchoRequest
from pyof.v0x04.symmetric.experimenter import ExperimenterHeader
from pyof.v0x04.symmetric.hello import Hello

__all__ = ('MESSAGE_TYPES', 'new_message_from_header',
           'new_message_from_message_type', 'unpack_message')

MESSAGE_TYPES = {

    # Symetric/Immutable messages
    str(Type.OFPT_HELLO): Hello,
    str(Type.OFPT_ERROR): ErrorMsg,
    str(Type.OFPT_ECHO_REQUEST): EchoRequest,
    str(Type.OFPT_ECHO_REPLY): EchoReply,
    str(Type.OFPT_EXPERIMENTER): ExperimenterHeader,

    # Switch configuration messages
    # Controller/Switch messages
    str(Type.OFPT_FEATURES_REQUEST): FeaturesRequest,
    str(Type.OFPT_FEATURES_REPLY): FeaturesReply,
    str(Type.OFPT_GET_CONFIG_REQUEST): GetConfigRequest,
    str(Type.OFPT_GET_CONFIG_REPLY): GetConfigReply,
    str(Type.OFPT_SET_CONFIG): SetConfig,

    # Async messages
    str(Type.OFPT_PACKET_IN): PacketIn,
    str(Type.OFPT_FLOW_REMOVED): FlowRemoved,
    str(Type.OFPT_PORT_STATUS): PortStatus,

    # Controller command messages
    # Controller/Switch message
    str(Type.OFPT_PACKET_OUT): PacketOut,
    str(Type.OFPT_FLOW_MOD): FlowMod,
    str(Type.OFPT_GROUP_MOD): GroupMod,
    str(Type.OFPT_PORT_MOD): PortMod,
    str(Type.OFPT_TABLE_MOD): TableMod,

    # Multipart messages.
    # Controller/Switch message
    str(Type.OFPT_MULTIPART_REPLY): MultipartReply,
    str(Type.OFPT_MULTIPART_REQUEST): MultipartRequest,

    # Barrier messages
    # Controller/Switch message
    str(Type.OFPT_BARRIER_REQUEST): BarrierRequest,
    str(Type.OFPT_BARRIER_REPLY): BarrierReply,

    # Queue Configuration messages
    # Controller/Switch message
    str(Type.OFPT_QUEUE_GET_CONFIG_REQUEST): QueueGetConfigRequest,
    str(Type.OFPT_QUEUE_GET_CONFIG_REPLY): QueueGetConfigReply,

    # Controller role change request message
    # Controller/Switch message
    str(Type.OFPT_ROLE_REQUEST): RoleRequest,
    str(Type.OFPT_ROLE_REPLY): RoleReply,

    # Asynchronous message configuration
    # Controller/Switch message
    str(Type.OFPT_GET_ASYNC_REQUEST): GetAsyncRequest,
    str(Type.OFPT_GET_ASYNC_REPLY): GetAsyncReply,
    str(Type.OFPT_SET_ASYNC): SetAsync,

    # Meters and rate limiters configuration messages
    # Controller/Switch message
    str(Type.OFPT_METER_MOD): MeterMod,
}


def new_message_from_message_type(message_type):
    """Given an OpenFlow Message Type, return an empty message of that type.

    Args:
        messageType (:class:`~pyof.v0x04.common.header.Type`):
            Python-openflow message.

    Returns:
        Empty OpenFlow message of the requested message type.

    Raises:
        KytosUndefinedMessageType: Unkown Message_Type.

    """
    message_type = str(message_type)
    if message_type not in MESSAGE_TYPES:
        msg = "Define class for {} in {}".format(message_type, __file__)
        raise ValueError(msg)

    message_class = MESSAGE_TYPES.get(message_type)
    message_instance = message_class()

    return message_instance


def new_message_from_header(header):
    """Given an OF Header, return an empty message of header's message_type.

    Args:
        header (:class:`~pyof.v0x04.common.header.Header`):
            Unpacked OpenFlow Header.

    Returns:
        Empty OpenFlow message of the same type of message_type attribute from
        the given header.
        The header attribute of the message will be populated.

    Raises:
        KytosUndefinedMessageType: Unkown Message_Type.

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


def unpack_message(buffer):
    """Unpack the whole buffer, including header pack.

    Args:
        buffer (bytes): Bytes representation of a openflow message.

    Returns:
        object: Instance of openflow message.

    """
    hdr_size = Header().get_size()
    hdr_buff, msg_buff = buffer[:hdr_size], buffer[hdr_size:]
    header = Header()
    header.unpack(hdr_buff)
    message = new_message_from_header(header)
    message.unpack(msg_buff)
    return message
