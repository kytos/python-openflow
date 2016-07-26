"""Defines common structures and enums for controller2switch."""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import action
from pyof.v0x01.common import flow_match
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


# Enums


class ConfigFlags(enum.Enum):
    """Configuration Flags. Handling of IP Fragments."""

    #: No special handling for fragments
    OFPC_FRAG_NORMAL = 0
    #: Drop fragments
    OFPC_FRAG_DROP = 1
    #: Reassemble (only if OFPC_IP_REASM set)
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


class StatsTypes(enum.Enum):
    """Type field to be used both in both request and reply.

    It specifies the kind of information being passed and determines how the
    body field is interpreted.
    """

    #: Description of this OpenFlow switch. The request body is empty.
    OFPST_DESC = 1
    #: Individual flow statistics. The request body is struct
    #: ofp_flow_stats_request.
    OFPST_FLOW = 2
    #: Aggregate flow statistics. The request body is struct
    #: ofp_aggregate_stats_request.
    OFPST_AGGREGATE = 3
    #: Flow table statistics. The request body is empty.
    OFPST_TABLE = 4
    #: Physical port statistics. The request body is empty.
    OFPST_PORT = 5
    #: Queue statistics for a port. The request body defines the port
    OFPST_QUEUE = 6
    #: Vendor extension. The request and reply bodies begin with a 32-bit
    #: vendor ID
    OFPST_VENDOR = 0xffff


# Classes


class SwitchConfig(base.GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages.

    Args:
        xid (int): xid to be used on the message header.
        flags (ConfigFlags): OFPC_* flags.
        miss_send_len (int): UBInt16 max bytes of new flow that the datapath
            should send to the controller.
    """

    header = of_header.Header()
    flags = basic_types.UBInt16(enum_ref=ConfigFlags)
    miss_send_len = basic_types.UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.flags = flags
        self.miss_send_len = miss_send_len


class ListOfActions(basic_types.FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and used on ActionHeader objects.

    Args:
        items (ActionHeader): Instance or a list of instances.
    """

    def __init__(self, items=None):
        super().__init__(pyof_class=action.ActionHeader, items=items)


class AggregateStatsReply(base.GenericStruct):
    """Body of reply to OFPST_AGGREGATE request.

    Args:
        packet_count (int): Number of packets in flows
        byte_count (int):   Number of bytes in flows
        flow_count (int):   Number of flows
    """

    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()
    flow_count = basic_types.UBInt32()
    #: Align to 64 bits
    pad = basic_types.PAD(4)

    def __init__(self, packet_count=None, byte_count=None, flow_count=None):
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.flow_count = flow_count


class AggregateStatsRequest(base.GenericStruct):
    """Body for ofp_stats_request of type OFPST_AGGREGATE.

    Args:
        match (Match): Fields to match.
        table_id (int): ID of table to read (from pyof_table_stats) 0xff for
            all tables or 0xfe for emergency.
        out_port (int): Require matching entries to include this as an output
            port. A value of OFPP_NONE indicates no restriction.
    """

    match = flow_match.Match()
    table_id = basic_types.UBInt8()
    #: Align to 32 bits
    pad = basic_types.PAD(1)
    out_port = basic_types.UBInt16()

    def __init__(self, match=None, table_id=None, out_port=None):
        super().__init__()
        self.match = match
        self.table_id = table_id
        self.out_port = out_port


class DescStats(base.GenericStruct):
    """Information available from the OFPST_DESC stats request.

    Information about the switch manufacturer, hardware revision, software
    revision, serial number and a description field.

    Args:
        mfr_desc (str): Manufacturer description
        hw_desc (str): Hardware description
        sw_desc (str): Software description
        serial_num (str): Serial number
        dp_desc (str): Human readable description of datapath
    """

    mfr_desc = basic_types.Char(length=base.DESC_STR_LEN)
    hw_desc = basic_types.Char(length=base.DESC_STR_LEN)
    sw_desc = basic_types.Char(length=base.DESC_STR_LEN)
    serial_num = basic_types.Char(length=base.SERIAL_NUM_LEN)
    dp_desc = basic_types.Char(length=base.DESC_STR_LEN)

    def __init__(self, mfr_desc=None, hw_desc=None, sw_desc=None,
                 serial_num=None, dp_desc=None):
        super().__init__()
        self.mfr_desc = mfr_desc
        self.hw_desc = hw_desc
        self.sw_desc = sw_desc
        self.serial_num = serial_num
        self.dp_desc = dp_desc


class FlowStats(base.GenericStruct):
    """Body of reply to OFPST_FLOW request.

    Args:
        length (int): Length of this entry.
        table_id (int): ID of table flow came from.
        match (Match): Description of fields.
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
        actions (ListOfActions): Actions.
    """

    length = basic_types.UBInt16()
    table_id = basic_types.UBInt8()
    #: Align to 32 bits.
    pad = basic_types.PAD(1)
    match = flow_match.Match()
    duration_sec = basic_types.UBInt32()
    duration_nsec = basic_types.UBInt32()
    priority = basic_types.UBInt16()
    idle_timeout = basic_types.UBInt16()
    hard_timeout = basic_types.UBInt16()
    #: Align to 64-bits
    pad2 = basic_types.PAD(6)
    cookie = basic_types.UBInt64()
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()
    actions = ListOfActions()

    def __init__(self, length=None, table_id=None, match=None,
                 duration_sec=None, duration_nsec=None, priority=None,
                 idle_timeout=None, hard_timeout=None, cookie=None,
                 packet_count=None, byte_count=None, actions=None):
        super().__init__()
        self.length = length
        self.table_id = table_id
        self.match = match
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.prioriry = priority
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.cookie = cookie
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.actions = [] if actions is None else actions


class FlowStatsRequest(base.GenericStruct):
    """Body for ofp_stats_request of type OFPST_FLOW.

    Args:
        match (Match): Fields to match.
        table_id (int): ID of table to read (from pyof_table_stats)
            0xff for all tables or 0xfe for emergency.
        out_port (:class:`int`, :class:`.Port`): Require matching entries to
            include this as an output port. A value of :attr:`.Port.OFPP_NONE`
            indicates no restriction.
    """

    match = flow_match.Match()
    table_id = basic_types.UBInt8()
    #: Align to 32 bits.
    pad = basic_types.PAD(1)
    out_port = basic_types.UBInt16()

    def __init__(self, match=None, table_id=None, out_port=None):
        super().__init__()
        self.match = match
        self.table_id = table_id
        self.out_port = out_port


class PortStats(base.GenericStruct):
    """Body of reply to OFPST_PORT request.

    If a counter is unsupported, set the field to all ones.

    Args:
        port_no (:class:`int`, :class:`.Port`): Port number.
        rx_packets (int): Number of received packets.
        tx_packets (int): Number of transmitted packets.
        rx_bytes (int): Number of received bytes.
        tx_bytes (int): Number of transmitted bytes.
        rx_dropped (int): Number of packets dropped by RX.
        tx_dropped (int): Number of packets dropped by TX.
        rx_errors (int): Number of receive errors. This is a super-set of more
            specific receive errors and should be greater than or equal to the
            sum of all rx_*_err values.
        tx_errors (int): Number of transmit errors.  This is a super-set of
            more specific transmit errors and should be greater than or equal
            to the sum of all tx_*_err values (none currently defined).
        rx_frame_err (int): Number of frame alignment errors.
        rx_over_err (int): Number of packets with RX overrun.
        rx_crc_err (int): Number of CRC errors.
        collisions (int): Number of collisions.
    """

    port_no = basic_types.UBInt16()
    #: Align to 64-bits.
    pad = basic_types.PAD(6)
    rx_packets = basic_types.UBInt64()
    tx_packets = basic_types.UBInt64()
    rx_bytes = basic_types.UBInt64()
    tx_bytes = basic_types.UBInt64()
    rx_dropped = basic_types.UBInt64()
    tx_dropped = basic_types.UBInt64()
    rx_errors = basic_types.UBInt64()
    tx_errors = basic_types.UBInt64()
    rx_frame_err = basic_types.UBInt64()
    rx_over_err = basic_types.UBInt64()
    rx_crc_err = basic_types.UBInt64()
    collisions = basic_types.UBInt64()

    def __init__(self, port_no=None, rx_packets=None,
                 tx_packets=None, rx_bytes=None, tx_bytes=None,
                 rx_dropped=None, tx_dropped=None, rx_errors=None,
                 tx_errors=None, rx_frame_err=None, rx_over_err=None,
                 rx_crc_err=None, collisions=None):
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


class PortStatsRequest(base.GenericStruct):
    """Body for ofp_stats_request of type OFPST_PORT.

    Args:
        port_no (:class:`int`, :class:`.Port`): OFPST_PORT message must request
            statistics either for a single port (specified in port_no) or for
            all ports (if port_no == :attr:`.Port.OFPP_NONE`).
    """

    port_no = basic_types.UBInt16()
    #: Align to 64-bits.
    pad = basic_types.PAD(6)

    def __init__(self, port_no=None):
        super().__init__()
        self.port_no = port_no


class QueueStats(base.GenericStruct):
    """Implements the reply body of a port_no.

    Args:
        port_no (:class:`int`, :class:`.Port`): Port Number.
        queue_id (int): Queue ID.
        tx_bytes (int): Number of transmitted bytes.
        tx_packets (int): Number of transmitted packets.
        tx_errors (int): Number of packets dropped due to overrun.
    """

    port_no = basic_types.UBInt16()
    #: Align to 32-bits.
    pad = basic_types.PAD(2)
    queue_id = basic_types.UBInt32()
    tx_bytes = basic_types.UBInt64()
    tx_packets = basic_types.UBInt64()
    tx_errors = basic_types.UBInt64()

    def __init__(self, port_no=None, queue_id=None, tx_bytes=None,
                 tx_packets=None, tx_errors=None):
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id
        self.tx_bytes = tx_bytes
        self.tx_packets = tx_packets
        self.tx_errors = tx_errors


class QueueStatsRequest(base.GenericStruct):
    """Implements the request body of a ``port_no``.

    Args:
        port_no (:class:`int`, :class:`.Port`): All ports if
            :attr:`.Port.OFPP_ALL`.
        queue_id (int): All queues if OFPQ_ALL.
    """

    port_no = basic_types.UBInt16()
    #: Align to 32-bits
    pad = basic_types.PAD(2)
    queue_id = basic_types.UBInt32()

    def __init__(self, port_no=None, queue_id=None):
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id


class TableStats(base.GenericStruct):
    """Body of reply to OFPST_TABLE request.

    Args:
        table_id (int): Identifier of table.  Lower numbered tables are
            consulted first.
        name (str): Table name.
        wildcards (FlowWildCards): Bitmap of OFPFW_* wildcards that are
            supported by the table.
        max_entries (int): Max number of entries supported.
        active_count (int): Number of active entries.
        count_lookup (int): Number of packets looked up in table.
        count_matched (int): Number of packets that hit table.
    """

    table_id = basic_types.UBInt8()
    #: Align to 32-bits.
    pad = basic_types.PAD(3)
    name = basic_types.Char(length=base.OFP_MAX_TABLE_NAME_LEN)
    wildcards = basic_types.UBInt32(enum_ref=flow_match.FlowWildCards)
    max_entries = basic_types.UBInt32()
    active_count = basic_types.UBInt32()
    count_lookup = basic_types.UBInt64()
    count_matched = basic_types.UBInt64()

    def __init__(self, table_id=None, name=None, wildcards=None,
                 max_entries=None, active_count=None, count_lookup=None,
                 count_matched=None):
        super().__init__()
        self.table_id = table_id
        self.name = name
        self.wildcards = wildcards
        self.max_entries = max_entries
        self.active_count = active_count
        self.count_lookup = count_lookup
        self.count_matched = count_matched
