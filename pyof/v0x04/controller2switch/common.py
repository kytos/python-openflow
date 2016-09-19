"""Defines common structures and enums for controller2switch."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import (Char, FixedTypeList, Pad, UBInt8,
                                         UBInt16, UBInt32, UBInt64)
from pyof.foundation.constants import DESC_STR_LEN, SERIAL_NUM_LEN
from pyof.v0x04.asynchronous.flow_removed import FlowRemovedReason
from pyof.v0x04.asynchronous.packet_in import PacketInReason
from pyof.v0x04.asynchronous.port_status import PortReason
from pyof.v0x04.common.action import ActionHeader
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header

# Third-party imports

__all__ = ('AggregateStatsReply', 'AggregateStatsRequest', 'ConfigFlags',
           'ControllerRole', 'DescStats', 'FlowStats', 'FlowStatsRequest',
           'ListOfActions', 'MultipartTypes', 'PortStats', 'PortStatsRequest',
           'QueueStats', 'QueueStatsRequest', 'StatsTypes', 'TableStats')

# Enums


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


class MultipartTypes(Enum):
    """Types of Multipart Messages, both Request and Reply."""

    #: Description of this OpenFlow switch.
    #: The request body is empty.
    #: The reply body is struct ofp_desc.
    OFPMP_DESC = 0

    #: Individual flow statistics.
    #: The request body is struct ofp_flow_stats_request.
    #: The reply body is an array of struct ofp_flow_stats.
    OFPMP_FLOW = 1

    #: Aggregate flow statistics.
    #: The request body is struct ofp_aggregate_stats_request.
    #: The reply body is struct ofp_aggregate_stats_reply.
    OFPMP_AGGREGATE = 2

    #: Flow table statistics.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_table_stats.
    OFPMP_TABLE = 3

    #: Port statistics.
    #: The request body is struct ofp_port_stats_request.
    #: The reply body is an array of struct ofp_port_stats.
    OFPMP_PORT_STATS = 4

    #: Queue statistics for a port.
    #: The request body is struct ofp_queue_stats_request.
    #: The reply body is an array of struct ofp_queue_stats.
    OFPMP_QUEUE = 5

    #: Group counter statistics.
    #: The request body is struct ofp_group_stats_request.
    #: The reply is an array of struct ofp_group_stats.
    OFPMP_GROUP = 6

    #: Group description.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_group_desc_stats.
    OFPMP_GROUP_DESC = 7

    #: Group features.
    #: The request body is empty.
    #: The reply body is struct ofp_group_features.
    OFPMP_GROUP_FEATURES = 8

    #: Meter statistics.
    #: The request body is struct ofp_meter_multipart_requests.
    #: The reply body is an array of struct ofp_meter_stats.
    OFPMP_METER = 9

    #: Meter configuration.
    #: The request body is struct ofp_meter_multipart_requests.
    #: The reply body is an array of struct ofp_meter_config.
    OFPMP_METER_CONFIG = 10

    #: Meter features.
    #: The request body is empty.
    #: The reply body is struct ofp_meter_features.
    OFPMP_METER_FEATURES = 11

    #: Table features.
    #: The request body is either empty or contains an array of
    #: struct ofp_table_features containing the controller’s desired view of
    #: the switch. If the switch is unable to set the specified view an error
    #: is returned.
    #: The reply body is an array of struct ofp_table_features.
    OFPMP_TABLE_FEATURES = 12

    #: Port description.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_port.
    OFPMP_PORT_DESC = 13

    #: Experimenter extension.
    #: The request and reply bodies begin with
    #: struct ofp_experimenter_multipart_header.
    #: The request and reply bodies are otherwise experimenter-defined.
    OFPMP_EXPERIMENTER = 0xffff


class StatsTypes(Enum):
    """Type field to be used both in both request and reply.

    It specifies the kind of information being passed and determines how the
    body field is interpreted.
    """

    #: Description of this OpenFlow switch. The request body is empty.
    OFPST_DESC = 0
    #: Individual flow statistics. The request body is struct
    #: ofp_flow_stats_request.
    OFPST_FLOW = 1
    #: Aggregate flow statistics. The request body is struct
    #: ofp_aggregate_stats_request.
    OFPST_AGGREGATE = 2
    #: Flow table statistics. The request body is empty.
    OFPST_TABLE = 3
    #: Physical port statistics. The request body is empty.
    OFPST_PORT = 4
    #: Queue statistics for a port. The request body defines the port
    OFPST_QUEUE = 5
    #: Vendor extension. The request and reply bodies begin with a 32-bit
    #: vendor ID
    OFPST_VENDOR = 0xffff


# Classes


class AggregateStatsReply(GenericStruct):
    """Body of reply to OFPMP_AGGREGATE request."""

    #: Number of packets in flows.
    packet_count = UBInt64()
    #: Number of bytes in flows.
    byte_count = UBInt64()
    #: Number of flows.
    flow_count = UBInt32()
    #: Align to 64 bits
    pad = Pad(4)

    def __init__(self, packet_count=None, byte_count=None, flow_count=None):
        """The constructor just assings parameters to object attributes.

        Args:
            packet_count (int): Number of packets in flows
            byte_count (int):   Number of bytes in flows
            flow_count (int):   Number of flows
        """
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.flow_count = flow_count


class AggregateStatsRequest(GenericStruct):
    """Body for ofp_stats_request of type OFPST_AGGREGATE."""

    #: ID of table to read (from ofp_table_stats) OFPTT_ALL for all tables.
    table_id = UBInt8()
    #: Align to 32 bits.
    pad = Pad(3)
    #: Require matching entries to include this as an output port. A value of
    #: OFPP_ANY indicates no restriction.
    out_port = UBInt32()
    #: Require matching entries to include this as an output group. A value of
    #: OFPG_ANY indicates no restriction.
    out_group = UBInt32()
    #: Align to 64 bits
    pad2 = Pad(4)
    #: Require matching entries to contain this cookie value
    cookie = UBInt64()
    #: Mask used to restrict the cookie bits that must match. A value of 0
    #: indicates no restriction.
    cookie_mask = UBInt64()
    #: Fields to match. Variable size.
    match = Match()

    def __init__(self, table_id=None, out_port=None, out_group=None,
                 cookie=None, cookie_mask=None, match=None):
        """The constructor just assings parameters to object attributes.

        Args:
            table_id (int): ID of table to read (from ofp_table_stats)
                OFPTT_ALL for all tables.
            out_port (int): Require matching entries to include this as an
                output port. A value of OFPP_ANY indicates no restriction.
            out_group (in): Require matching entries to include this as an
                output group. A value of OFPG_ANY indicates no restriction.
            cookie (int): Require matching entries to contain this cookie value
            cookie_mask (int): Mask used to restrict the cookie bits that must
                match. A value of 0 indicates no restriction.
            match (Match): Fields to match. Variable size
        """
        super().__init__()
        self.table_id = table_id
        self.out_port = out_port
        self.out_group = out_group
        self.cookie = cookie
        self.cookie_mask = cookie_mask
        self.match = match


class DescStats(GenericStruct):
    """Information available from the OFPST_DESC stats request.

    Information about the switch manufacturer, hardware revision, software
    revision, serial number and a description field.
    """

    #: Manufacturer description
    mfr_desc = Char(length=DESC_STR_LEN)
    #: Hardware description
    hw_desc = Char(length=DESC_STR_LEN)
    #: Software description
    sw_desc = Char(length=DESC_STR_LEN)
    #: Serial number
    serial_num = Char(length=SERIAL_NUM_LEN)

    def __init__(self, mfr_desc=None, hw_desc=None, sw_desc=None,
                 serial_num=None):
        """The constructor just assings parameters to object attributes.

        Args:
            mfr_desc (str): Manufacturer description
            hw_desc (str): Hardware description
            sw_desc (str): Software description
            serial_num (str): Serial number
        """
        super().__init__()
        self.mfr_desc = mfr_desc
        self.hw_desc = hw_desc
        self.sw_desc = sw_desc
        self.serial_num = serial_num


class FlowStats(GenericStruct):
    """Body of reply to OFPST_FLOW request."""

    length = UBInt16()
    table_id = UBInt8()
    #: Align to 32 bits.
    pad = Pad(1)
    duration_sec = UBInt32()
    duration_nsec = UBInt32()
    priority = UBInt16()
    idle_timeout = UBInt16()
    hard_timeout = UBInt16()
    flags = UBInt16()
    #: Align to 64-bits
    pad2 = Pad(4)
    cookie = UBInt64()
    packet_count = UBInt64()
    byte_count = UBInt64()
    match = Match()

    def __init__(self, length=None, table_id=None, duration_sec=None,
                 duration_nsec=None, priority=None, idle_timeout=None,
                 hard_timeout=None, flags=None, cookie=None, packet_count=None,
                 byte_count=None, match=None):
        """The constructor just assings parameters to object attributes.

        Args:
            length (int): Length of this entry.
            table_id (int): ID of table flow came from.
            duration_sec (int): Time flow has been alive in seconds.
            duration_nsec (int): Time flow has been alive in nanoseconds in
                addition to duration_sec.
            priority (int): Priority of the entry. Only meaningful when this
                is not an exact-match entry.
            idle_timeout (int): Number of seconds idle before expiration.
            hard_timeout (int): Number of seconds before expiration.
            cookie (int): Opaque controller-issued identifier.
            packet_count (int): Number of packets in flow.
            byte_count (int): Number of bytes in flow.
            match (Match): Description of fields.
        """
        super().__init__()
        self.length = length
        self.table_id = table_id
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.priority = priority
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.flags = flags
        self.cookie = cookie
        self.packet_count = packet_count
        self.byte_count = byte_count


class FlowStatsRequest(GenericStruct):
    """Body for ofp_stats_request of type OFPST_FLOW."""

    table_id = UBInt8()
    #: Align to 32 bits.
    pad = Pad(3)
    out_port = UBInt32()
    out_group = UBInt32()
    pad2 = Pad(4)
    cookie = UBInt64()
    cookie_mask = UBInt64()
    match = Match()

    def __init__(self, table_id=None, out_port=None, out_group=None,
                 cookie=None, cookie_mask=None, match=None):
        """The constructor just assings parameters to object attributes.

        Args:
            table_id (int): ID of table to read (from pyof_table_stats)
                0xff for all tables or 0xfe for emergency.
            out_port (:class:`int`, :class:`.Port`): Require matching entries
                to include this as an output port. A value of
                :attr:`.Port.OFPP_NONE` indicates no restriction.
            out_group: Require matching entries to include this as an output
                group. A value of OFPG_ANY indicates no restriction.
            cookie: Requires matching entries to contain this cookie value
            cookie_mask: Mask used to restrict the cookie bits that must match.
                A value of 0 indicates no restriction.
            match (Match): Fields to match.
        """
        super().__init__()
        self.table_id = table_id
        self.out_port = out_port
        self.out_group = out_group
        self.cookie = cookie
        self.cookie_mask = cookie_mask
        self.match = match


class ListOfActions(FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and used on ActionHeader objects.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (ActionHeader): Instance or a list of instances.
        """
        super().__init__(pyof_class=ActionHeader, items=items)


class PortStats(GenericStruct):
    """Body of reply to OFPST_PORT request.

    If a counter is unsupported, set the field to all ones.
    """

    port_no = UBInt32()
    #: Align to 64-bits.
    pad = Pad(4)
    rx_packets = UBInt64()
    tx_packets = UBInt64()
    rx_bytes = UBInt64()
    tx_bytes = UBInt64()
    rx_dropped = UBInt64()
    tx_dropped = UBInt64()
    rx_errors = UBInt64()
    tx_errors = UBInt64()
    rx_frame_err = UBInt64()
    rx_over_err = UBInt64()
    rx_crc_err = UBInt64()
    collisions = UBInt64()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()

    def __init__(self, port_no=None, rx_packets=None,
                 tx_packets=None, rx_bytes=None, tx_bytes=None,
                 rx_dropped=None, tx_dropped=None, rx_errors=None,
                 tx_errors=None, rx_frame_err=None, rx_over_err=None,
                 rx_crc_err=None, collisions=None, duration_sec=None,
                 duration_nsec=None):
        """The constructor assigns parameters to object attributes.

        Args:
            port_no (:class:`int`, :class:`.Port`): Port number.
            rx_packets (int): Number of received packets.
            tx_packets (int): Number of transmitted packets.
            rx_bytes (int): Number of received bytes.
            tx_bytes (int): Number of transmitted bytes.
            rx_dropped (int): Number of packets dropped by RX.
            tx_dropped (int): Number of packets dropped by TX.
            rx_errors (int): Number of receive errors. This is a super-set of
                more specific receive errors and should be greater than or
                equal to the sum of all rx_*_err values.
            tx_errors (int): Number of transmit errors.  This is a super-set of
                more specific transmit errors and should be greater than or
                equal to the sum of all tx_*_err values (none currently
                defined).
            rx_frame_err (int): Number of frame alignment errors.
            rx_over_err (int): Number of packets with RX overrun.
            rx_crc_err (int): Number of CRC errors.
            collisions (int): Number of collisions.
            duration_sec (int): Time port has been alive in seconds
            duration_nsec (int): Time port has been alive in nanoseconds beyond
                duration_sec
        """
        super().__init__()
        self.port_no = port_no
        self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_dropped = rx_dropped
        self.tx_dropped = tx_dropped
        self.rx_errors = rx_errors
        self.tx_errors = tx_errors
        self.rx_frame_err = rx_frame_err
        self.rx_over_err = rx_over_err
        self.rx_crc_err = rx_crc_err
        self.collisions = collisions
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec


class PortStatsRequest(GenericStruct):
    """Body for ofp_stats_request of type OFPST_PORT."""

    port_no = UBInt16()
    #: Align to 64-bits.
    pad = Pad(6)

    def __init__(self, port_no=None):
        """The constructor just assings parameters to object attributes.

        Args:
            port_no (:class:`int`, :class:`.Port`): OFPST_PORT message must
                request statistics either for a single port (specified in
                ``port_no``) or for all ports (if port_no ==
                :attr:`.Port.OFPP_NONE`).
        """
        super().__init__()
        self.port_no = port_no


class QueueStats(GenericStruct):
    """Implements the reply body of a port_no."""

    port_no = UBInt32()
    queue_id = UBInt32()
    tx_bytes = UBInt64()
    tx_packets = UBInt64()
    tx_errors = UBInt64()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()

    def __init__(self, port_no=None, queue_id=None, tx_bytes=None,
                 tx_packets=None, tx_errors=None, duration_sec=None,
                 duration_nsec=None):
        """The constructor just assings parameters to object attributes.

        Args:
            port_no (:class:`int`, :class:`.Port`): Port Number.
            queue_id (int): Queue ID.
            tx_bytes (int): Number of transmitted bytes.
            tx_packets (int): Number of transmitted packets.
            tx_errors (int): Number of packets dropped due to overrun.
            duration_sec (int): Time queue has been alive in seconds.
            duration_nsec (int): Time queue has been alive in nanoseconds
                beyond duration_sec.
        """
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id
        self.tx_bytes = tx_bytes
        self.tx_packets = tx_packets
        self.tx_errors = tx_errors
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec


class QueueStatsRequest(GenericStruct):
    """Implements the request body of a ``port_no``."""

    port_no = UBInt32()
    queue_id = UBInt32()

    def __init__(self, port_no=None, queue_id=None):
        """The constructor just assings parameters to object attributes.

        Args:
            port_no (:class:`int`, :class:`.Port`): All ports if
                :attr:`.Port.OFPP_ALL`.
            queue_id (int): All queues if OFPQ_ALL.
        """
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id


class TableStats(GenericStruct):
    """Body of reply to OFPST_TABLE request."""

    table_id = UBInt8()
    #: Align to 32-bits.
    pad = Pad(3)
    active_count = UBInt32()
    lookup_count = UBInt64()
    matched_count = UBInt64()

    def __init__(self, table_id=None, name=None, max_entries=None,
                 active_count=None, lookup_count=None,
                 matched_count=None):
        """The constructor just assings parameters to object attributes.

        Args:
            table_id (int): Identifier of table.  Lower numbered tables are
                consulted first.
            active_count (int): Number of active entries.
            lookup_count (int): Number of packets looked up in table.
            matched_count (int): Number of packets that hit table.
        """
        super().__init__()
        self.table_id = table_id
        self.active_count = active_count
        self.lookup_count = lookup_count
        self.matched_count = matched_count


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
