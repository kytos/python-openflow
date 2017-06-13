"""Controller replying state from datapath."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericBitMask, GenericMessage, GenericStruct
from pyof.foundation.basic_types import (
    BinaryData, Char, FixedTypeList, Pad, UBInt8, UBInt16, UBInt32, UBInt64)
from pyof.foundation.constants import DESC_STR_LEN, SERIAL_NUM_LEN
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import Port
from pyof.v0x04.controller2switch.common import (
    Bucket, BucketCounter, ExperimenterMultipartHeader, MultipartTypes,
    TableFeatures)
from pyof.v0x04.controller2switch.meter_mod import (
    ListOfMeterBandHeader, MeterBandType, MeterFlags)

# Third-party imports


__all__ = ('MultipartReply', 'MultipartReplyFlags', 'AggregateStatsReply',
           'Desc', 'FlowStats', 'PortStats', 'QueueStats', 'GroupDescStats',
           'GroupFeatures', 'GroupStats', 'MeterConfig', 'MeterFeatures',
           'BandStats', 'ListOfBandStats', 'MeterStats', 'GroupCapabilities',
           'TableStats')

# Enum


class MultipartReplyFlags(Enum):
    """Flags for MultipartReply."""

    #: More replies to follow.
    OFPMPF_REPLY_MORE = 1 << 0


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

# Classes


class MultipartReply(GenericMessage):
    """Reply datapath state.

    While the system is running, the controller may reply state from the
    datapath using the OFPT_MULTIPART_REPLY message.
    """

    #: Openflow :class:`~pyof.v0x04.common.header.Header`
    header = Header(message_type=Type.OFPT_MULTIPART_REPLY)
    #: One of the OFPMP_* constants.
    multipart_type = UBInt16(enum_ref=MultipartTypes)
    #: OFPMPF_REPLY_* flags.
    flags = UBInt16(enum_ref=MultipartReplyFlags)
    #: Padding
    pad = Pad(4)
    #: Body of the reply
    body = BinaryData()

    def __init__(self, xid=None, multipart_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to the header.
            multipart_type (int): One of the OFPMP_* constants.
            flags (int): OFPMPF_REPLY_* flags.
            body (bytes): Body of the reply.
        """
        super().__init__(xid)
        self.multipart_type = multipart_type
        self.flags = flags
        self.body = body

    def pack(self, value=None):
        """Pack a StatsReply using the object's attributes.

        This method will pack the attribute body and multipart_type before pack
        the StatsReply object, then will return this struct as a binary data.

        Returns:
            stats_reply_packed (bytes): Binary data with StatsReply packed.
        """
        buff = self.body
        if not value:
            value = self.body

        if value:
            if isinstance(value, (list, FixedTypeList)):
                obj = self._get_body_instance()
                obj.extend(value)
            elif hasattr(value, 'pack'):
                obj = value

            self.body = obj.pack()

        multiparty_packed = super().pack()
        self.body = buff

        return multiparty_packed

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``body`` attribute which has its type determined
        by the ``multipart_type`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
        """
        super().unpack(buff[offset:])
        self._unpack_body()

    def _unpack_body(self):
        """Unpack `body` replace it by the result."""
        obj = self._get_body_instance()
        obj.unpack(self.body.value)
        self.body = obj

    def _get_body_instance(self):
        """Method used to return the body instance."""
        exp_header = ExperimenterMultipartHeader
        simple_body = {MultipartTypes.OFPMP_DESC: Desc,
                       MultipartTypes.OFPMP_GROUP_FEATURES: GroupFeatures,
                       MultipartTypes.OFPMP_METER_FEATURES: MeterFeatures,
                       MultipartTypes.OFPMP_EXPERIMENTER: exp_header}

        array_of_bodies = {MultipartTypes.OFPMP_FLOW: FlowStats,
                           MultipartTypes.OFPMP_AGGREGATE: AggregateStatsReply,
                           MultipartTypes.OFPMP_TABLE: TableStats,
                           MultipartTypes.OFPMP_PORT_STATS: PortStats,
                           MultipartTypes.OFPMP_QUEUE: QueueStats,
                           MultipartTypes.OFPMP_GROUP: GroupStats,
                           MultipartTypes.OFPMP_GROUP_DESC: GroupDescStats,
                           MultipartTypes.OFPMP_METER: MeterStats,
                           MultipartTypes.OFPMP_METER_CONFIG: MeterConfig,
                           MultipartTypes.OFPMP_TABLE_FEATURES: TableFeatures,
                           MultipartTypes.OFPMP_PORT_DESC: Port}

        if isinstance(self.multipart_type, (int, UBInt16)):
            self.multipart_type = self.multipart_type.enum_ref(
                self.multipart_type.value)

        pyof_class = simple_body.get(self.multipart_type, None)
        if pyof_class:
            return pyof_class()

        array_of_class = array_of_bodies.get(self.multipart_type, None)
        if array_of_class:
            return FixedTypeList(pyof_class=pyof_class)

        return BinaryData(b'')


# MultipartReply Body

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


class Desc(GenericStruct):
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
            match (~pyof.v0x04.common.flow_match.Match): Description of fields.
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

    # Can't avoid "too many local variables" (R0914) in this struct.
    # pylint: disable=R0914
    def __init__(self, port_no=None, rx_packets=None,
                 tx_packets=None, rx_bytes=None, tx_bytes=None,
                 rx_dropped=None, tx_dropped=None, rx_errors=None,
                 tx_errors=None, rx_frame_err=None, rx_over_err=None,
                 rx_crc_err=None, collisions=None, duration_sec=None,
                 duration_nsec=None):
        """The constructor assigns parameters to object attributes.

        Args:
            port_no (:class:`int`, :class:`~pyof.v0x04.common.port.Port`):
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
            port_no (:class:`int`, :class:`~pyof.v0x04.common.port.Port`):
                Port Number.
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
    capabilities = UBInt32(enum_ref=GroupCapabilities)
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


class MeterConfig(GenericStruct):
    """MeterConfig is a class to represent ofp_meter_config structure.

    Body of reply to OFPMP_METER_CONFIG request.
    """

    # Length of this entry.
    length = UBInt16()
    # All OFPMC_* that apply.
    flags = UBInt16(enum_ref=MeterFlags)
    # Meter instance or OFPM_ALL .
    meter_id = UBInt32()
    # The bands length is inferred from the length field.
    bands = ListOfMeterBandHeader()

    def __init__(self, flags=MeterFlags.OFPMF_STATS, meter_id=None,
                 bands=None):
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
        self.bands = bands if bands else []


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
        super().__init__()
        self.max_meter = max_meter
        self.band_types = band_types
        self.capabilities = capabilities
        self.max_bands = max_bands
        self.max_color = max_color


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
        super().__init__()
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
        super().__init__(pyof_class=BandStats, items=items)


class MeterStats(GenericStruct):
    """Meter Statistics.

    Body of reply to OFPMP_METER request.
    """

    meter_id = UBInt32()
    length = UBInt16()
    pad = Pad(6)
    flow_count = UBInt32()
    packet_in_count = UBInt64()
    byte_in_count = UBInt64()
    duration_sec = UBInt32()
    duration_nsec = UBInt32()
    band_stats = ListOfBandStats()

    def __init__(self, meter_id=None, flow_count=None,
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
        self.packet_in_count = packet_in_count
        self.byte_in_count = byte_in_count
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.band_stats = band_stats if band_stats else []
        self.update_length()

    def update_length(self):
        """Update length attribute with current struct length."""
        self.length = self.get_size()

    def pack(self, value=None):
        """Pack method used to update the length of instance and packing.

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
        length.unpack(buff, offset)

        length.unpack(buff, offset=offset+MeterStats.meter_id.get_size())
        super().unpack(buff[:offset+length.value], offset=offset)


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
