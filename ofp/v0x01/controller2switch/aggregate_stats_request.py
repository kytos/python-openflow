"""Aggregate information about multiple flows is requested with the
OFPST_AGGREGATE stats request type"""

# System imports

# Third-party imports

# Local source tree imports
from common import flow_match
from foundation import base
from foundation import basic_types


class AggregateStatsRequest(base.GenericStruct):
    """
    Body for ofp_stats_request of type OFPST_AGGREGATE

        :param match -- Fields to match
        :param table_id -- ID of table to read (from ofp_table_stats) 0xff
                           for all tables or 0xfe for emergency.
        :param pad -- Align to 32 bits
        :param out_port -- Require matching entries to include this as an
                           output port.  A value of OFPP_NONE indicates
                           no restriction

    """
    match = flow_match.OFPMatch()
    table_id = basic_types.UBInt8()
    pad = basic_types.UBInt8()
    out_port = basic_types.UBInt16()

    def __init__(self, match=None, table_id=None, pad=None, out_port=None):

        self.match = match
        self.table_id = table_id
        self.pad = pad
        self.out_port = out_port
