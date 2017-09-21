"""Request a change of the role of the controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.constants import UBINT64_MAX_VALUE
from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.common import ControllerRole, RoleBaseMessage

__all__ = ('RoleReply',)

# Classes


class RoleReply(RoleBaseMessage):
    """RoleReply Message."""

    def __init__(self, xid=None, role=ControllerRole.OFPCR_ROLE_NOCHANGE,
                 generation_id=UBINT64_MAX_VALUE):
        """Create a RoleReply with the optional parameters below.

        Args:
            xid (int): OpenFlow xid to the header.
            role (:class:`~.controller2switch.common.ControllerRole`):
                Is the new role that the controller wants to assume.
            generation_id (int): Master Election Generation Id. The default
                value is -1. For this field, it's UBINT64_MAX_VALUE.
        """
        super().__init__(xid, role, generation_id)
        self.header.message_type = Type.OFPT_ROLE_REPLY
