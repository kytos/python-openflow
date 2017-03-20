"""Module with generic messages used in controller2switch."""

# System imports
from enum import Enum

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import Pad, UBInt16, UBInt32, UBInt64
from pyof.v0x04.asynchronous.flow_removed import FlowRemovedReason
from pyof.v0x04.asynchronous.packet_in import PacketInReason
from pyof.v0x04.asynchronous.port_status import PortReason
from pyof.v0x04.common.header import Header

__all__ = ('ConfigFlags', 'ControllerRole',)


class ConfigFlags(Enum):
    """Handling of IP fragments."""

    #: No special handling for fragments.
    OFPC_FRAG_NORMAL = 0
    #: Drop fragments.
    OFPC_FRAG_DROP = 1
    #: Reassemble (only if OFPC_IP_REASM set).
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


class ControllerRole(Enum):
    """Controller roles."""

    #: Don’t change current role.
    OFPCR_ROLE_NOCHANGE = 0
    #: Default role, full access.
    OFPCR_ROLE_EQUAL = 1
    #: Full access, at most one master.
    OFPCR_ROLE_MASTER = 2
    #: Read-only access.
    OFPCR_ROLE_SLAVE = 3

# Base Classes for other messages - not meant to be directly used, so, because
# of that, they will not be inserted on the __all__ attribute.


class AsyncConfig(GenericMessage):
    """Asynchronous message configuration base class.

    Common structure for SetAsync and GetAsyncReply messages.

    AsyncConfig contains three 2-element arrays. Each array controls whether
    the controller receives asynchronous messages with a specific
    :class:`~.common.header.Type`. Within each array, element 0 specifies
    messages of interest when the controller has a OFPCR_ROLE_EQUAL or
    OFPCR_ROLE_MASTER role; element 1, when the controller has a
    OFPCR_ROLE_SLAVE role. Each array element is a bit-mask in which a 0-bit
    disables receiving a message sent with the reason code corresponding to the
    bit index and a 1-bit enables receiving it.
    """

    #: OpenFlow :class:`~common.header.Header`
    #: OFPT_GET_ASYNC_REPLY or OFPT_SET_ASYNC.
    header = Header()
    packet_in_mask1 = UBInt32(enum_ref=PacketInReason)
    packet_in_mask2 = UBInt32(enum_ref=PacketInReason)
    port_status_mask1 = UBInt32(enum_ref=PortReason)
    port_status_mask2 = UBInt32(enum_ref=PortReason)
    flow_removed_mask1 = UBInt32(enum_ref=FlowRemovedReason)
    flow_removed_mask2 = UBInt32(enum_ref=FlowRemovedReason)

    def __init__(self, xid=None, packet_in_mask1=None, packet_in_mask2=None,
                 port_status_mask1=None, port_status_mask2=None,
                 flow_removed_mask1=None, flow_removed_mask2=None):
        """Base class for Asynchronous configuration messages.

        Common structure for SetAsync and GetAsyncReply messages.

        Args:
            xid (int): xid to be used on the message header.
            packet_in_mask1 (): .
            packet_in_mask2 (): .
            port_status_mask1 (): .
            port_status_mask2 (): .
            flow_removed_mask1 (): .
            flow_removed_mask2 (): .
        """
        super().__init__(xid)
        self.packet_in_mask1 = packet_in_mask1
        self.packet_in_mask2 = packet_in_mask2
        self.port_status_mask1 = port_status_mask1
        self.port_status_mask2 = port_status_mask2
        self.flow_removed_mask1 = flow_removed_mask1
        self.flow_removed_mask2 = flow_removed_mask2


class RoleBaseMessage(GenericMessage):
    """Role basic structure for RoleRequest and RoleReply messages."""

    #: :class:`~.common.header.Header`
    #: Type OFPT_ROLE_REQUEST/OFPT_ROLE_REPLY.
    header = Header()
    #: One of NX_ROLE_*. (:class:`~.controller2switch.common.ControllerRole`)
    role = UBInt32(enum_ref=ControllerRole)
    #: Align to 64 bits.
    pad = Pad(4)
    #: Master Election Generation Id.
    generation_id = UBInt64()

    def __init__(self, xid=None, role=None, generation_id=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): OpenFlow xid to the header.
            role (:class:`~.controller2switch.common.ControllerRole`): .
            generation_id (int): Master Election Generation Id.
        """
        super().__init__(xid)
        self.role = role
        self.generation_id = generation_id


class SwitchConfig(GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages."""

    #: OpenFlow :class:`~common.header.Header`
    header = Header()
    flags = UBInt16(enum_ref=ConfigFlags)
    miss_send_len = UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            flags (ConfigFlags): OFPC_* flags.
            miss_send_len (int): UBInt16 max bytes of new flow that the
                datapath should send to the controller.
        """
        super().__init__(xid)
        self.flags = flags
        self.miss_send_len = miss_send_len
