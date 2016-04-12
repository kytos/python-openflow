"""Response the stat request packet from the controller"""

# System imports

# Third-party imports

# Local source tree imports
from common import header as of_header
from foundation import base
from foundation import basic_types


class StatsReply(base.GenericStruct):
    """
    Class implements the response to the config request

        :param header -- OpenFlow header
        :param type -- One of the OFPST_* constants
        :param flags -- OFPSF_REQ_* flags (none yet defined)
        :param body -- Body of the request
    """
    header = of_header.OFPHeader()
    type = basic_types.UBInt16()
    flags = basic_types.UBInt16()
    body = basic_types.UBInt8Array(length=0)

    def __init__(self, header=None, type=None, flags=None, body=None):

        self.header = header
        self.type = type
        self.flags = flags
        self.body = body
