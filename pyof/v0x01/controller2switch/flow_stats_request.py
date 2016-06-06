"""Information about individual flows"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import flow_match
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Classes


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
        self.match = match
        self.table_id = table_id
        self.out_port = out_port
