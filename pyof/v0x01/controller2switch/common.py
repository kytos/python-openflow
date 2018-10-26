"""Defines common structures and enums for controller2switch."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, Char, Pad, UBInt8, UBInt16, UBInt32, UBInt64)
from pyof.foundation.constants import (
    DESC_STR_LEN, OFP_MAX_TABLE_NAME_LEN, SERIAL_NUM_LEN)
# Local source tree imports
from pyof.v0x01.common.action import ListOfActions
from pyof.v0x01.common.flow_match import FlowWildCards, Match
from pyof.v0x01.common.header import Header
from pyof.v0x01.common.phy_port import Port

# Third-party imports

__all__ = ('ConfigFlag', 'StatsType', 'AggregateStatsReply',
           'AggregateStatsRequest', 'DescStats', 'FlowStats',
           'FlowStatsRequest', 'PortStats', 'PortStatsRequest', 'QueueStats',
           'QueueStatsRequest', 'TableStats', 'VendorStats',
           'VendorStatsRequest')

# Enums


class ConfigFlag(IntEnum):
    """Configuration Flags. Handling of IP Fragments."""

    #: No special handling for fragments
    OFPC_FRAG_NORMAL = 0
    #: Drop fragments
    OFPC_FRAG_DROP = 1
    #: Reassemble (only if OFPC_IP_REASM set)
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


class StatsType(IntEnum):
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


class SwitchConfig(GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages."""

    header = Header()
    flags = UBInt16(enum_ref=ConfigFlag)
    miss_send_len = UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        """Create a SwitchConfig with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            flags (ConfigFlag): OFPC_* flags.
            miss_send_len (int): UBInt16 max bytes of new flow that the
                datapath should send to the controller.
        """
        super().__init__(xid)
        self.flags = flags
        self.miss_send_len = miss_send_len

    def __repr__(self):
        """Show a full representation of the object."""
        return "%s(xid=%r, flags=%s, miss_send_len=%r)" \
               % (self.__class__.__name__, self.header.xid, self.flags,
                  self.miss_send_len)


class AggregateStatsReply(GenericStruct):
    """Body of reply to OFPST_AGGREGATE request."""

    packet_count = UBInt64()
    byte_count = UBInt64()
    flow_count = UBInt32()
    #: Align to 64 bits
    pad = Pad(4)

    def __init__(self, packet_count=None, byte_count=None, flow_count=None):
        """Create a AggregateStatsReply with the optional parameters below.

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

    match = Match()
    table_id = UBInt8()
    #: Align to 32 bits
    pad = Pad(1)
    out_port = UBInt16()

    def __init__(self, match=Match(), table_id=0xff, out_port=Port.OFPP_NONE):
        """Create a AggregateStatsRequest with the optional parameters below.

        Args:
            match (~pyof.v0x01.common.flow_match.Match): Fields to match.
            table_id (int): ID of table to read (from pyof_table_stats) 0xff
                for all tables or 0xfe for emergency.
            out_port (int): Require matching entries to include this as an
                output port. A value of OFPP_NONE indicates no restriction.
        """
        super().__init__()
        self.match = match
        self.table_id = table_id
        self.out_port = out_port


class DescStats(GenericStruct):
    """Information available from the OFPST_DESC stats request.

    Information about the switch manufacturer, hardware revision, software
    revision, serial number and a description field.
    """

    mfr_desc = Char(length=DESC_STR_LEN)
    hw_desc = Char(length=DESC_STR_LEN)
    sw_desc = Char(length=DESC_STR_LEN)
    serial_num = Char(length=SERIAL_NUM_LEN)
    dp_desc = Char(length=DESC_STR_LEN)

    def __init__(self, mfr_desc=None, hw_desc=None, sw_desc=None,
                 serial_num=None, dp_desc=None):
        """Create a DescStats with the optional parameters below.

        Args:
            mfr_desc (str): Manufacturer description
            hw_desc (str): Hardware description
            sw_desc (str): Software description
            serial_num (str): Serial number
            dp_desc (str): Human readable description of datapath
        """
        super().__init__()
        self.mfr_desc = mfr_desc
        self.hw_desc = hw_desc
        self.sw_desc = sw_desc
        self.serial_num = serial_num
        self.dp_desc = dp_desc


class FlowStats(GenericStruct):
    """Body of reply to OFPST_FLOW request."""

    length = UBInt16()
    table_id = UBInt8()
    #: Align to 32 bits.
    pad = Pad(1)
    match = Match()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()
    priority = UBInt16()
    idle_timeout = UBInt16()
    hard_timeout = UBInt16()
    #: Align to 64-bits
    pad2 = Pad(6)
    cookie = UBInt64()
    packet_count = UBInt64()
    byte_count = UBInt64()
    actions = ListOfActions()

    def __init__(self, length=None, table_id=None, match=None,
                 duration_sec=None, duration_nsec=None, priority=None,
                 idle_timeout=None, hard_timeout=None, cookie=None,
                 packet_count=None, byte_count=None, actions=None):
        """Create a FlowStats with the optional parameters below.

        Args:
            length (int): Length of this entry.
            table_id (int): ID of table flow came from.
            match (~pyof.v0x01.common.flow_match.Match): Description of fields.
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
            actions (:class:`~pyof.v0x01.common.actions.ListOfActions`):
                List of Actions.
        """
        super().__init__()
        self.length = length
        self.table_id = table_id
        self.match = match
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.priority = priority
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.cookie = cookie
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.actions = [] if actions is None else actions

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        Do nothing, since the _length is already defined and it is just a Pad.
        Keep buff and offset just for compability with other unpack methods.

        Args:
            buff (bytes): Buffer where data is located.
            offset (int): Where data stream begins.
        """
        self.length = UBInt16()
        self.length.unpack(buff, offset)
        max_length = offset + self.length.value
        super().unpack(buff[:max_length], offset)


class FlowStatsRequest(GenericStruct):
    """Body for ofp_stats_request of type OFPST_FLOW."""

    match = Match()
    table_id = UBInt8()
    #: Align to 32 bits.
    pad = Pad(1)
    out_port = UBInt16()

    def __init__(self, match=None, table_id=0xff, out_port=Port.OFPP_NONE):
        """Create a FlowStatsRequest with the optional parameters below.

        Args:
            match (:class:`~pyof.v0x01.common.flow_match.Match`):
                Fields to match.
            table_id (int): ID of table to read (from pyof_table_stats)
                0xff for all tables or 0xfe for emergency.
            out_port (:class:`int`, :class:`~pyof.v0x01.common.phy_port.Port`):
                Require matching entries to include this as an output port.
                A value of :attr:`.Port.OFPP_NONE` indicates no restriction.
        """
        super().__init__()
        self.match = Match() if match is None else match
        self.table_id = table_id
        self.out_port = out_port


class PortStats(GenericStruct):
    """Body of reply to OFPST_PORT request.

    If a counter is unsupported, set the field to all ones.
    """

    port_no = UBInt16()
    #: Align to 64-bits.
    pad = Pad(6)
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

    def __init__(self, port_no=None, rx_packets=None,
                 tx_packets=None, rx_bytes=None, tx_bytes=None,
                 rx_dropped=None, tx_dropped=None, rx_errors=None,
                 tx_errors=None, rx_frame_err=None, rx_over_err=None,
                 rx_crc_err=None, collisions=None):
        """Create a PortStats with the optional parameters below.

        Args:
            port_no (:class:`int`, :class:`~pyof.v0x01.common.phy_port.Port`):
                Port number.
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


class PortStatsRequest(GenericStruct):
    """Body for ofp_stats_request of type OFPST_PORT."""

    port_no = UBInt16()
    #: Align to 64-bits.
    pad = Pad(6)

    def __init__(self, port_no=None):
        """Create a PortStatsRequest with the optional parameters below.

        Args:
            port_no (:class:`int`, :class:`~pyof.v0x01.common.phy_port.Port`):
                OFPST_PORT message must request statistics either for a single
                port (specified in ``port_no``) or for all ports
                (if ``port_no`` == :attr:`.Port.OFPP_NONE`).
        """
        super().__init__()
        self.port_no = port_no


class QueueStats(GenericStruct):
    """Implements the reply body of a port_no."""

    port_no = UBInt16()
    #: Align to 32-bits.
    pad = Pad(2)
    queue_id = UBInt32()
    tx_bytes = UBInt64()
    tx_packets = UBInt64()
    tx_errors = UBInt64()

    def __init__(self, port_no=None, queue_id=None, tx_bytes=None,
                 tx_packets=None, tx_errors=None):
        """Create a QueueStats with the optional parameters below.

        Args:
            port_no (:class:`int`, :class:`~pyof.v0x01.common.phy_port.Port`):
                Port Number.
            queue_id (int): Queue ID.
            tx_bytes (int): Number of transmitted bytes.
            tx_packets (int): Number of transmitted packets.
            tx_errors (int): Number of packets dropped due to overrun.
        """
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id
        self.tx_bytes = tx_bytes
        self.tx_packets = tx_packets
        self.tx_errors = tx_errors


class QueueStatsRequest(GenericStruct):
    """Implements the request body of a ``port_no``."""

    port_no = UBInt16()
    #: Align to 32-bits
    pad = Pad(2)
    queue_id = UBInt32()

    def __init__(self, port_no=None, queue_id=None):
        """Create a QueueStatsRequest with the optional parameters below.

        Args:
            port_no (:class:`int`, :class:`~pyof.v0x01.common.phy_port.Port`):
                 All ports if :attr:`.Port.OFPP_ALL`.
            queue_id (int): All queues if OFPQ_ALL (``0xfffffff``).
        """
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id


class TableStats(GenericStruct):
    """Body of reply to OFPST_TABLE request."""

    table_id = UBInt8()
    #: Align to 32-bits.
    pad = Pad(3)
    name = Char(length=OFP_MAX_TABLE_NAME_LEN)
    wildcards = UBInt32(enum_ref=FlowWildCards)
    max_entries = UBInt32()
    active_count = UBInt32()
    count_lookup = UBInt64()
    count_matched = UBInt64()

    def __init__(self, table_id=None, name=None, wildcards=None,
                 max_entries=None, active_count=None, count_lookup=None,
                 count_matched=None):
        """Create a TableStats with the optional parameters below.

        Args:
            table_id (int): Identifier of table.  Lower numbered tables are
                consulted first.
            name (str): Table name.
            wildcards (:class:`~pyof.v0x01.common.flow_match.FlowWildCards`):
                Bitmap of OFPFW_* wildcards that are supported by the table.
            max_entries (int): Max number of entries supported.
            active_count (int): Number of active entries.
            count_lookup (int): Number of packets looked up in table.
            count_matched (int): Number of packets that hit table.
        """
        super().__init__()
        self.table_id = table_id
        self.name = name
        self.wildcards = wildcards
        self.max_entries = max_entries
        self.active_count = active_count
        self.count_lookup = count_lookup
        self.count_matched = count_matched


class VendorStats(GenericStruct):
    """Vendor extension."""

    vendor = UBInt32()
    body = BinaryData()

    def __init__(self, vendor=None, body=b''):
        """Create instance attributes.

        Args:
            vendor (int): 32-bit vendor ID.
            body (bytes): Vendor-defined body
        """
        super().__init__()
        self.vendor = vendor
        self.body = body


VendorStatsRequest = VendorStats
