"""Query the datapath about its current state."""

# System imports

# Third-party imports

from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base, basic_types

__all__ = ('StatsRequest',)


class StatsRequest(base.GenericMessage):
    """Response to the config request."""

    #: OpenFlow :class:`.Header`
    header = of_header.Header(message_type=of_header.Type.OFPT_STATS_REQUEST)
    body_type = basic_types.UBInt16(enum_ref=common.StatsTypes)
    flags = basic_types.UBInt16()
    body = basic_types.ConstantTypeList()

    def __init__(self, xid=None, body_type=None, flags=None, body=None):
        """The constructor just assings parameters to object attributes.

        Args:
            body_type (StatsTypes): One of the OFPST_* constants.
            flags (int): OFPSF_REQ_* flags (none yet defined).
            body (ConstantTypeList): Body of the request.
        """
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.body_type = body_type
        self.flags = flags
        self.body = [] if body is None else body
