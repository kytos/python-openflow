"""Query the datapath about its current state."""

# System imports

# Third-party imports

from importlib import import_module

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
# Local imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import StatsType

__all__ = ('StatsRequest',)


class StatsRequest(GenericMessage):
    """Request statistics to switch."""

    #: OpenFlow :class:`~pyof.v0x01.common.header.Header`
    header = Header(message_type=Type.OFPT_STATS_REQUEST)
    body_type = UBInt16(enum_ref=StatsType)
    flags = UBInt16()
    body = BinaryData()

    def __init__(self, xid=None, body_type=None, flags=0, body=b''):
        """Create a StatsRequest with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            body_type (StatsType): One of the OFPST_* constants.
            flags (int): OFPSF_REQ_* flags (none yet defined).
            body (BinaryData): Body of the request.
        """
        super().__init__(xid)
        self.body_type = body_type
        self.flags = flags
        self.body = body

    def pack(self, value=None):
        """Pack according to :attr:`body_type`.

        Make `body` a binary pack before packing this object. Then, restore
        body.
        """
        backup = self.body
        if not value:
            value = self.body

        if hasattr(value, 'pack'):
            self.body = value.pack()
        stats_request_packed = super().pack()

        self.body = backup
        return stats_request_packed

    def unpack(self, buff, offset=0):
        """Unpack according to :attr:`body_type`."""
        super().unpack(buff)

        class_name = self._get_body_class()
        buff = self.body.value
        self.body = FixedTypeList(pyof_class=class_name)
        self.body.unpack(buff)

    def _get_body_class(self):
        if isinstance(self.body_type, (int, UBInt16)):
            self.body_type = self.body_type.enum_ref(self.body_type.value)

        module = import_module('pyof.v0x01.controller2switch.common')
        body_name = self.body_type.name.replace('OFPST_', '').title()

        for class_name in module.__all__:
            if 'Request' in class_name and body_name in class_name:
                return getattr(module, class_name)
        return None
