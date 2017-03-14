"""Defines common structures and enums for controller2switch."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericMessage, GenericStruct
from pyof.foundation.basic_types import (Char, FixedTypeList, Pad, UBInt8,
                                         UBInt16, UBInt32, UBInt64)
from pyof.foundation.constants import DESC_STR_LEN, SERIAL_NUM_LEN
from pyof.v0x04.controller2switch.meter_mod import MeterBandType, MeterFlags
from pyof.v0x04.asynchronous.flow_removed import FlowRemovedReason
from pyof.v0x04.asynchronous.packet_in import PacketInReason
from pyof.v0x04.asynchronous.port_status import PortReason
from pyof.v0x04.controller2switch.meter_mod import Meter
from pyof.v0x04.common.action import ActionHeader
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header
from pyof.v0x04.controller2switch.meter_mod import (Meter, MeterFlags,
                                                    MeterBandHeader,
                                                    ListOfMeterBandHeader)

# Third-party imports


__all__ = ('AggregateStatsReply', 'AggregateStatsRequest', 'Bucket',
           'BucketCounter', 'ConfigFlags', 'ControllerRole', 'DescStats',
           'FlowStats', 'FlowStatsRequest', 'GroupCapabilities',
           'ExperimenterMultipartHeader', 'GroupDescStats',
           'GroupFeatures', 'GroupStats', 'GroupStatsRequest', 
           'ListOfActions', 'MultipartTypes', 'PortStats',
           'PortStatsRequest', 'QueueStats', 'QueueStatsRequest', 'StatsTypes',
           'TableStats', 'MeterMultipartRequest', 'MeterConfig',
           'MeterFeatures', 'BandStats', 'ListOfBandStats', 'MeterStats')

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


class GroupCapabilities(GenericBitMask):
    """Group configuration flags."""

    #: Support weight for select groups.
    OFPGFC_SELECT_WEIGHT = 1 << 0
    #: Support liveness for select groups.
    OFPGFC_SELECT_LIVENESS = 1 << 1
    #: Support chaining groups.
    OFPGFC_CHAINING = 1 << 2
    #: Chack chaining for loops and delete.
    OFPGFC_CHAINING_CHECKS = 1 << 3


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


class Bucket(GenericStruct):
    """Bucket for use in groups."""

    length = UBInt16()
    weight = UBInt16()
    watch_port = UBInt32()
    watch_group = UBInt32()
    pad = Pad(4)
    actions = FixedTypeList(ActionHeader)

    def __init__(self, length=None, weight=None, watch_port=None,
                 watch_group=None, actions=None):
        """Initialize all instance variables.

        Args:
            length (int): Length the bucket in bytes, including this header and
                any padding to make it 64-bit aligned.
            weight (int): Relative weight of bucket. Only defined for select
                groups.
            watch_port (int): Port whose state affects whether this bucket is
                live. Only required for fast failover groups.
            watch_group (int): Group whose state affects whether this bucket is
                live. Only required for fast failover groups.
            actions (:func:`list` of :class:`.ActionHeader`): The action length
                is inferred from the length field in the header.
        """
        super().__init__()
        self.length = length
        self.weight = weight
        self.watch_port = watch_port
        self.watch_group = watch_group
        self.actions = actions


class BucketCounter(GenericStruct):
    """Used in group stats replies."""

    #: Number of packets processed by bucket.
    packet_count = UBInt64()
    #: Number of bytes processed by bucket.
    byte_count = UBInt64()

    def __init__(self, packet_count=None, byte_count=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            packet_count: Number of packets processed by bucket.
            byte_count: Number of bytes processed by bucket.
        """
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count


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
    #: Datapath description
    dp_desc = Char(length=DESC_STR_LEN)

    def __init__(self, mfr_desc=None, hw_desc=None, sw_desc=None,
                 serial_num=None, dp_desc=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            mfr_desc (str): Manufacturer description
            hw_desc (str): Hardware description
            sw_desc (str): Software description
            serial_num (str): Serial number
            dp_desc (str): Datapath description
        """
        super().__init__()
        self.mfr_desc = mfr_desc
        self.hw_desc = hw_desc
        self.sw_desc = sw_desc
        self.serial_num = serial_num
        self.dp_desc = dp_desc


class ExperimenterMultipartHeader(GenericStruct):
    """Body for ofp_multipart_request/reply of type OFPMP_EXPERIMENTER."""

    experimenter = UBInt32()
    exp_type = UBInt32()
    #: Followed by experimenter-defined arbitrary data.

    def __init__(self, experimenter=None, exp_type=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            experimenter: Experimenter ID which takes the same form as in
                struct ofp_experimenter_header (class ExperimenterHeader).
            exp_type: Experimenter defined.
        """
        super().__init__()
        self.experimenter = experimenter
        self.exp_type = exp_type


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


class GroupDescStats(GenericStruct):
    """Body of reply to OFPMP_GROUP_DESC request."""

    length = UBInt16()
    group_type = UBInt8()
    #: Pad to 64 bits.
    pad = Pad(1)
    group_id = UBInt32()
    buckets = FixedTypeList(Bucket)

    def __init__(self, length=None, group_type=None, group_id=None,
                 buckets=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            length: Length of this entry.
            group_type: One of OFPGT_*.
            group_id: Group identifier.
            buckets: List of buckets in group.
        """
        super().__init__()
        self.length = length
        self.group_type = group_type
        self.group_id = group_id
        self.buckets = buckets


class GroupFeatures(GenericStruct):
    """Body of reply to OFPMP_GROUP_FEATURES request.Group features."""

    types = UBInt32()
    capabilities = UBInt32()
    max_groups1 = UBInt32()
    max_groups2 = UBInt32()
    max_groups3 = UBInt32()
    max_groups4 = UBInt32()
    actions1 = UBInt32()
    actions2 = UBInt32()
    actions3 = UBInt32()
    actions4 = UBInt32()

    def __init__(self, types=None, capabilities=None, max_groups1=None,
                 max_groups2=None, max_groups3=None, max_groups4=None,
                 actions1=None, actions2=None, actions3=None, actions4=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            types: Bitmap of OFPGT_* values supported.
            capabilities: Bitmap of OFPGFC_* capability supported.
            max_groups: 4-position array; Maximum number of groups for each
                type.
            actions: 4-position array; Bitmaps of OFPAT_* that are supported.
        """
        super().__init__()
        self.types = types
        self.capabilities = capabilities
        self.max_groups1 = max_groups1
        self.max_groups2 = max_groups2
        self.max_groups3 = max_groups3
        self.max_groups4 = max_groups4
        self.actions1 = actions1
        self.actions2 = actions2
        self.actions3 = actions3
        self.actions4 = actions4


class GroupStats(GenericStruct):
    """Body of reply to OFPMP_GROUP request."""

    length = UBInt16()
    #: Align to 64 bits.
    pad = Pad(2)
    group_id = UBInt32()
    ref_count = UBInt32()
    #: Align to 64 bits.
    pad2 = Pad(4)
    packet_count = UBInt64()
    byte_count = UBInt64()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()
    bucket_stats = FixedTypeList(BucketCounter)

    def __init__(self, length=None, group_id=None, ref_count=None,
                 packet_count=None, byte_count=None, duration_sec=None,
                 duration_nsec=None, bucket_stats=None):
        """The constructor just assings parameters to object attributes.

        Args:
            length: Length of this entry
            group_id: Group identifier
            ref_count: Number of flows or groups that directly forward
                to this group.
            packet_count: Number of packets processed by group
            byte_count: Number of bytes processed by group
            duration_sec: Time group has been alive in seconds
            duration_nsec: Time group has been alive in nanoseconds
            bucket_stats: List of stats of group buckets
        """
        super().__init__()
        self.length = length
        self.group_id = group_id
        self.ref_count = ref_count
        self.packet_count = packet_count
        self.byte_count = byte_count
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.bucket_stats = bucket_stats


class GroupStatsRequest(GenericStruct):
    """Body of OFPMP_GROUP request."""

    #: Group id. All groups is OFPG_ALL
    group_id = UBInt32()
    #: Align to 64 bits
    pad = Pad(4)

    def __init__(self, group_id=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            group_id(int): ID of group to read. OFPG_ALL to request informatio
                for all groups.
        """
        super().__init__()
        self.group_id = group_id


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

    port_no = UBInt32()
    #: Align to 64-bits.
    pad = Pad(4)

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


class MeterMultipartRequest(GenericStruct):
    """MeterMultipartRequest structure.

    This class represents the structure for ofp_meter_multipart_request.
    This structure is a body of OFPMP_METER and OFPMP_METER_CONFIG requests.
    """

    # Meter instance, or OFPM_ALL.
    meter_id = UBInt32(enum_ref=Meter)

    # Align to 64 bits.
    pad = Pad(4)

    def __init__(self, meter_id=Meter.OFPM_ALL):
        """The Constructor of MeterMultipartRequest receives the paramters
        below.

        Args:
            meter_id(Meter): Meter Indentify.The value Meter.OFPM_ALL is used
                             to refer to all Meters on the switch.
        """

        super().__init__()
        self.meter_id = meter_id


class MeterConfig(GenericStruct):
    """MeterConfig is a class to represents  ofp_meter_config structure.

    Body of reply to OFPMP_METER_CONFIG request.
    """
    # Length of this entry.
    length = UBInt16()
    # All OFPMC_* that apply.
    flags = UBInt16(enum_ref=MeterFlags)
    # Meter instance.
    meter_id = UBInt32(enum_ref=Meter)
    # The bands length is inferred from the length field.
    bands = ListOfMeterBandHeader()

    def __init__(self, flags=MeterFlags.OFPMF_STATS, meter_id=Meter.OFPM_ALL,
                 bands=[]):
        """The Constructor of MeterConfig receives the parameters below.

        Args:
            flags(MeterFlags): Meter configuration flags.The default value is
                               MeterFlags.OFPMF_STATS
            meter_id(Meter):   Meter Indentify.The value Meter.OFPM_ALL is used
                               to refer to all Meters on the switch.
            bands(list):       List of MeterBandHeader instances.
        """
        super().__init__()
        self.flags = flags
        self.meter_id = meter_id
        self.bands = bands


class BandStats(GenericStruct):
    """Band  Statistics.

    Statistics for each meter band.
    """

    packet_band_count = UBInt64()
    byte_band_count = UBInt64()

    def __init__(self, packet_band_count=None, byte_band_count=None):
        """The constructor just assings parameters to object attributes.

        Args:
            packet_band_count(int): Number of packets in band.
            byte_band_count(int):   Number of bytes in band.
        """
        self.packet_band_count = packet_band_count
        self.byte_band_count = byte_band_count


class ListOfBandStats(FixedTypeList):
    """List of BandStats.

    Represented by instances of BandStats.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (BandStats): Instance or a list of instances.
        """
        super().__init__(pyof_class=BandStats,items=items)


class MeterStats(GenericStruct):
    """Meter Statistics.

    Body of reply to OFPMP_METER request.
    """

    meter_id = UBInt32(enum_ref=Meter)
    length = UBInt16()
    pad = Pad(6)
    flow_count = UBInt32()
    packet_in_count = UBInt64()
    byte_in_count = UBInt64()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()
    band_stats = ListOfBandStats()

    def __init__(self, meter_id=Meter.OFPM_ALL, flow_count=None,
                 packet_in_count=None, byte_in_count=None, duration_sec=None,
                 duration_nsec=None, band_stats=None):
        """The constructor just assings parameters to object attributes.

        Args:
            meter_id(Meter):      Meter instance.
            flow_count(int):      Number of flows bound to meter.
            packet_in_count(int): Number of packets in input.
            byte_in_count(int):   Number of bytes in input.
            duration_sec(int):    Time meter has been alive in seconds.
            duration_nsec(int):   Time meter has been alive in
                                  nanoseconds beyond duration_sec.
            band_stats(list):     Instances of BandStats
        """
        super().__init__()
        self.meter_id = meter_id
        self.flow_count = flow_count
        self.packet_in_count= packet_in_count
        self.byte_in_count = byte_in_count
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        if band_stats != None:
          self.band_stats = band_stats
        else:
           self.band_stats = []
        self.update_length()

    def update_length(self):
        self.length = self.get_size()


    def pack(self, value=None):
        """Pack method used to update the length of instance and  packing.

        Args:
            value: Structure to be packed.
        """
        self.update_length()
        return super().pack(value)

    def unpack(self, buff=None, offset=0):
        """Unpack *buff* into this object.
        This method will convert a binary data into a readable value according
        to the attribute format.
        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.
        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.
        """
        length = UBInt16()
        length.unpack(buff,offset)

        length.unpack(buff,offset=offset+MeterStats.meter_id.get_size())
        super().unpack(buff[:offset+length.value],offset=offset)


class MeterFeatures(GenericStruct):
    """Body of reply to OFPMP_METER_FEATURES request. Meter features."""

    max_meter = UBInt32()
    band_types = UBInt32(enum_ref=MeterBandType)
    capabilities = UBInt32(enum_ref=MeterFlags)
    max_bands = UBInt8()
    max_color = UBInt8()
    pad = Pad(2)

    def __init__(self, max_meter=None, band_types=None, capabilities=None,
                 max_bands=None, max_color=None):
        """The Constructor of MeterFeatures receives the parameters below.

        Args:
            max_meter(int):           Maximum number of meters.
            band_types(Meter):        Bitmaps of OFPMBT_* values supported.
            capabilities(MeterFlags): Bitmaps of "ofp_meter_flags".
            max_bands(int):           Maximum bands per meters
            max_color(int):           Maximum color value
        """
        self.max_meter = max_meter
        self.band_types = band_types
        self.capabilities = capabilities
        self.max_bands = max_bands
        self.max_color = max_color
