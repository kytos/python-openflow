"""Defines common structures and enums for controller2switch"""

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
    """Configuration Flags

        # Handling of IP Fragments
        OFPC_FRAG_NORMAL         # No special handling for fragments
        OFPC_FRAG_DROP           # Drop fragments
        OFPC_FRAG_REASM          # Reassemble (only if OFPC_IP_REASM set)
        OFPC_FRAG_MASK
    """
    OFPC_FRAG_NORMAL = 0
    OFPC_FRAG_DROP = 1
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


class StatsTypes(enum.Enum):
    """
    Class implements type field which is used both, request and reply. It
    specifies the kind of information being passed and determines how the
    body field is interpreted.

    Enums:

        OFPST_DESC = 1          # Description of this OpenFlow switch.
                                # The request body is empty.

        OFPST_FLOW = 2          # Individual flow statistics.
                                # The request body is struct
                                # ofp_flow_stats_request.

        OFPST_AGGREGATE = 3     # Aggregate flow statistics.
                                # The request body is struct
                                # ofp_aggregate_stats_request.

        OFPST_TABLE = 4         # Flow table statistics.
                                # The request body is empty.

        OFPST_PORT = 5          # Physical port statistics.
                                # The request body is empty.

        OFPST_QUEUE = 6         # Queue statistics for a port.
                                # The request body defines the port

        OFPST_VENDOR = 0xffff   # Vendor extension.
                                # The request and reply bodies begin with
                                # a 32-bit vendor ID
    """
    OFPST_DESC = 1
    OFPST_FLOW = 2
    OFPST_AGGREGATE = 3
    OFPST_TABLE = 4
    OFPST_PORT = 5
    OFPST_QUEUE = 6
    OFPST_VENDOR = 0xffff


# Classes


class SwitchConfig(base.GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages.

    :param xid:           xid to be used on the message header
    :param flags:         UBInt16 OFPC_* flags
    :param miss_send_len: UBInt16 max bytes of new flow that the
                          datapath should send to the controller
    """
    header = of_header.Header()
    flags = basic_types.UBInt16(enum_ref=ConfigFlags)
    miss_send_len = basic_types.UBInt16()

    def __init__(self, xid=None, flags=None, miss_send_len=None):
        super().__init__()
        self.header.xid = xid
        self.flags = flags
        self.miss_send_len = miss_send_len


class ListOfActions(basic_types.FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and
    used on ActionHeader objects

    Attributes:
        items (optional): Instance or a list of instances of ActionHeader
    """
    def __init__(self, items=None):
        super().__init__(pyof_class=action.ActionHeader, items=items)


class AggregateStatsReply(base.GenericStruct):
    """Body of reply to OFPST_AGGREGATE request.

    :param packet_count: Number of packets in flows
    :param byte_count:   Number of bytes in flows
    :param flow_count:   Number of flows
    :param pad:          Align to 64 bits

    """
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()
    flow_count = basic_types.UBInt32()
    pad = basic_types.PAD(4)

    def __init__(self, packet_count=None, byte_count=None, flow_count=None):
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.flow_count = flow_count


class AggregateStatsRequest(base.GenericStruct):
    """
    Body for ofp_stats_request of type OFPST_AGGREGATE.

    :param match:    Fields to match
    :param table_id: ID of table to read (from pyof_table_stats) 0xff
                     for all tables or 0xfe for emergency.
    :param pad:      Align to 32 bits
    :param out_port: Require matching entries to include this as an
                     output port.  A value of OFPP_NONE indicates
                     no restriction

    """
    match = flow_match.Match()
    table_id = basic_types.UBInt8()
    pad = basic_types.PAD(1)
    out_port = basic_types.UBInt16()

    def __init__(self, match=None, table_id=None, out_port=None):
        super().__init__()
        self.match = match
        self.table_id = table_id
        self.out_port = out_port


class DescStats(base.GenericStruct):
    """
    Information about the switch manufacturer, hardware revision, software
    revision, serial number, and a description field is avail- able from
    the OFPST_DESC stats request.

    :param mfr_desc:   Manufacturer description
    :param hw_desc:    Hardware description
    :param sw_desc:    Software description
    :param serial_num: Serial number
    :param dp_desc:    Human readable description of datapath

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
    """
    Body of reply to OFPST_FLOW request.

    :param length:        Length of this entry
    :param table_id:      ID of table flow came from
    :param pad:           Align to 32 bits
    :param match:         Description of fields
    :param duration_sec:  Time flow has been alive in seconds
    :param duration_nsec: Time flow has been alive in nanoseconds beyond
                          duration_sec
    :param priority:      Priority of the entry. Only meaningful when this
                          is not an exact-match entry
    :param idle_timeout:  Number of seconds idle before expiration
    :param hard_timeout:  Number of seconds before expiration
    :param pad2:          Align to 64-bits
    :param cookie:        Opaque controller-issued identifier
    :param packet_count:  Number of packets in flow
    :param byte_count:    Number of bytes in flow
    :param actions:       Actions
    """
    length = basic_types.UBInt16()
    table_id = basic_types.UBInt8()
    pad = basic_types.PAD(1)
    match = flow_match.Match()
    duration_sec = basic_types.UBInt32()
    duration_nsec = basic_types.UBInt32()
    priority = basic_types.UBInt16()
    idle_timeout = basic_types.UBInt16()
    hard_timeout = basic_types.UBInt16()
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
    """
    Body for ofp_stats_request of type OFPST_FLOW.

    :param match:    Fields to match
    :param table_id: ID of table to read (from pyof_table_stats)
                     0xff for all tables or 0xfe for emergency
    :param pad:      Align to 32 bits
    :param out_port: Require matching entries to include this as an output
                     port. A value of OFPP_NONE indicates no restriction.
    """
    match = flow_match.Match()
    table_id = basic_types.UBInt8()
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

    :param port_no:      Port number
    :param pad:          Align to 64-bits
    :param rx_packets:   Number of received packets
    :param tx_packets:   Number of transmitted packets
    :param rx_bytes:     Number of received bytes
    :param tx_bytes:     Number of transmitted bytes
    :param rx_dropped:   Number of packets dropped by RX
    :param tx_dropped:   Number of packets dropped by TX
    :param rx_errors:    Number of receive errors.  This is a super-set
                         of more specific receive errors and should be
                         greater than or equal to the sum of all
                         rx_*_err values
    :param tx_errors:    Number of transmit errors.  This is a super-set
                         of more specific transmit errors and should be
                         greater than or equal to the sum of all
                         tx_*_err values (none currently defined.)
    :param rx_frame_err: Number of frame alignment errors
    :param rx_over_err:  Number of packets with RX overrun
    :param rx_crc_err:   Number of CRC errors
    :param collisions:   Number of collisions

    """
    port_no = basic_types.UBInt16()
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
    """
    Body for ofp_stats_request of type OFPST_PORT

    :param port_no: OFPST_PORT message must request statistics either
                    for a single port (specified in port_no) or for
                    all ports (if port_no == OFPP_NONE).
    :param pad:

    """
    port_no = basic_types.UBInt16()
    pad = basic_types.PAD(6)

    def __init__(self, port_no=None):
        super().__init__()
        self.port_no = port_no


class QueueStats(base.GenericStruct):
    """
    Implements the reply body of a port_no

    :param port_no:    Port Number
    :param pad:        Align to 32-bits
    :param queue_id:   Queue ID
    :param tx_bytes:   Number of transmitted bytes
    :param tx_packets: Number of transmitted packets
    :param tx_errors:  Number of packets dropped due to overrun

    """
    port_no = basic_types.UBInt16()
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
    """
    Implements the request body of a port_no

    :param port_no:  All ports if OFPT_ALL
    :param pad:      Align to 32-bits
    :param queue_id: All queues if OFPQ_ALL
    """
    port_no = basic_types.UBInt16()
    pad = basic_types.PAD(2)
    queue_id = basic_types.UBInt32()

    def __init__(self, port_no=None, queue_id=None):
        super().__init__()
        self.port_no = port_no
        self.queue_id = queue_id


class TableStats(base.GenericStruct):
    """Body of reply to OFPST_TABLE request.

    :param table_id:      Identifier of table.  Lower numbered tables
                          are consulted first
    :param pad:           Align to 32-bits
    :param name:          Table name
    :param wildcards:     Bitmap of OFPFW_* wildcards that are supported
                          by the table
    :param max_entries:   Max number of entries supported
    :param active_count:  Number of active entries
    :param count_lookup:  Number of packets looked up in table
    :param count_matched: Number of packets that hit table

    """
    table_id = basic_types.UBInt8()
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
