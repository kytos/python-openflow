"""Response the stat request packet from the controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

__all__ = ['StatsReply']

# Classes


class StatsReply(base.GenericMessage):
    """Class implements the response to the config request.

    Args:
        body_type (StatsTypes): One of the OFPST_* constants.
        flags (int): OFPSF_REQ_* flags (none yet defined).
        body (ConstantTypeList): Body of the request.
    """

    #: OpenFlow :class:`.Header`
    header = of_header.Header(message_type=of_header.Type.OFPT_STATS_REPLY)
    body_type = basic_types.UBInt16(enum_ref=common.StatsTypes)
    flags = basic_types.UBInt16()
    body = basic_types.ConstantTypeList()

    def __init__(self, xid=None, body_type=None, flags=None, body=None):
        super().__init__()
        self.header.xid = xid
        self.body_type = body_type
        self.flags = flags
        self.body = [] if body is None else body
