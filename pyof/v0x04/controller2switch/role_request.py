"""Request a change of the role of the controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.common import RoleBaseMessage

__all__ = ('RoleRequest',)

# Classes


class RoleRequest(RoleBaseMessage):
    """RoleRequest Message.

    When the controller wants to change its role, it uses the OFPT_ROLE_REQUEST
    message.
    """

    def __init__(self, xid=None, role=None, generation_id=None):
        """Create a RoleRequest with the optional parameters below.

        Args:
            xid (int): OpenFlow xid to the header.
            role (:class:`~.controller2switch.common.ControllerRole`):
                Is the new role that the controller wants to assume.
            generation_id (int): Master Election Generation Id.
        """
        super().__init__(xid, role, generation_id)
        self.header.message_type = Type.OFPT_ROLE_REQUEST
