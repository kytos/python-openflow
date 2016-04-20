"""Query the datapath about its current state"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import header as of_header
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class StatsRequest(base.GenericStruct):
    """
    Class implements the response to the config request

        :param header -- OpenFlow header
        :param type -- One of the OFPST_* constants
        :param flags -- OFPSF_REQ_* flags (none yet defined)
        :param body -- Body of the request
    """
    header = of_header.OFPHeader()
    req_type = basic_types.UBInt16()
    flags = basic_types.UBInt16()
    body = None

    def __init__(self, header=None, req_type=None, flags=None, body=None):

        self.header = header
        self.req_type = req_type
        self.flags = flags
        if type(body) is list:
            self.body = basic_types.UBInt8Array(value=body, length=len(body))
