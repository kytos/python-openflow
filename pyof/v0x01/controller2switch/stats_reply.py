"""Response the stat request packet from the controller"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


# Enum


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


class StatsReply(base.GenericMessage):
    """
    Class implements the response to the config request

        :param header -- OpenFlow header
        :param body_type -- One of the OFPST_* constants
        :param flags -- OFPSF_REQ_* flags (none yet defined)
        :param body -- Body of the request
    """
    header = of_header.Header()
    body_type = basic_types.UBInt16()
    flags = basic_types.UBInt16()
    body = basic_types.ConstantTypeList()

    def __init__(self, xid=None, body_type=None, flags=None, body=[]):

        self.header.xid = xid
        self.header.message_type = of_header.Type.OFPT_STATS_REPLY
        self.body_type = body_type
        self.flags = flags
        self.body = body
