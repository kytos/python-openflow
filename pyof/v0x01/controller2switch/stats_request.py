"""Query the datapath about its current state"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class StatsRequest(base.GenericMessage):
    """Class implements the response to the config request

    :param header -- OpenFlow header
    :param body_type -- One of the OFPST_* constants
    :param flags -- OFPSF_REQ_* flags (none yet defined)
    :param body -- Body of the request

    """
    header = of_header.Header(message_type=of_header.Type.OFPT_STATS_REQUEST)
    body_type = basic_types.UBInt16(enum_ref=common.StatsTypes)
    flags = basic_types.UBInt16()
    body = basic_types.ConstantTypeList()

    def __init__(self, xid=None, body_type=None, flags=None, body=None):
        super().__init__()
        self.header.xid = xid
        self.body_type = body_type
        self.flags = flags
        self.body = [] if body is None else body
