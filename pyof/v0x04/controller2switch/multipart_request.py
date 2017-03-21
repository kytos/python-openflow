"""Controller requesting state from datapath."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import (BinaryData, Pad,
                                         UBInt8, UBInt16, UBInt32, UBInt64)
from pyof.v0x04.common.flow_match import Match
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.controller2switch.common import MultipartTypes

# Third-party imports


__all__ = ('MultipartRequest', 'MultipartRequestFlags',
           'AggregateStatsRequest', 'FlowStatsRequest', 'PortStatsRequest',
           'QueueStatsRequest', 'GroupStatsRequest', 'MeterMultipartRequest')

# Enum


class MultipartRequestFlags(Enum):
    """Flags for MultipartRequest."""

    #: More requests to follow
    OFPMPF_REQ_MORE = 1 << 0


# Classes


class MultipartRequest(GenericMessage):
    """Request datapath state.

    While the system is running, the controller may request state from the
    datapath using the OFPT_MULTIPART_REQUEST message.
    """

    #: :class:`~.common.header.Header`
    header = Header(message_type=Type.OFPT_MULTIPART_REQUEST)
    #: One of the OFPMP_* constants.
    multipart_type = UBInt16(enum_ref=MultipartTypes)
    #: OFPMPF_REQ_* flags.
    flags = UBInt16(enum_ref=MultipartRequestFlags)
    #: Padding
    pad = Pad(4)
    #: Body of the request
    body = BinaryData()

    def __init__(self, xid=None, multipart_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to the header.
            multipart_type (int): One of the OFPMP_* constants.
            flags (int): OFPMPF_REQ_* flags.
            body (bytes): Body of the request.
        """
        super().__init__(xid)
        self.multipart_type = multipart_type
        self.flags = flags
        self.body = body


# MultipartRequest body

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


class MeterMultipartRequest(GenericStruct):
    """MeterMultipartRequest structure.

    This class represents the structure for ofp_meter_multipart_request.
    This structure is a body of OFPMP_METER and OFPMP_METER_CONFIG requests.
    """

    # Meter instance, or OFPM_ALL.
    meter_id = UBInt32()

    # Align to 64 bits.
    pad = Pad(4)

    def __init__(self, meter_id=None):
        """Constructor of MeterMultipartRequest receives the parameters below.

        Args:
            meter_id(Meter): Meter Indentify.The value Meter.OFPM_ALL is used
                             to refer to all Meters on the switch.
        """
        super().__init__()
        self.meter_id = meter_id
