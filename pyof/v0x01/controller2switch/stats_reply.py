"""Response the stat request packet from the controller."""
from importlib import import_module

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import DescStats, StatsTypes

__all__ = ('StatsReply',)


class StatsReply(GenericMessage):
    """Class implements the response to the stats request."""

    #: OpenFlow :class:`~pyof.v0x01.common.header.Header`
    header = Header(message_type=Type.OFPT_STATS_REPLY)
    body_type = UBInt16(enum_ref=StatsTypes)
    flags = UBInt16()
    body = BinaryData()

    def __init__(self, xid=None, body_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            body_type (StatsTypes): One of the OFPST_* constants.
            flags (int): OFPSF_REQ_* flags (none yet defined).
            body (BinaryData): Body of the request.
        """
        super().__init__(xid)
        self.body_type = body_type
        self.flags = flags
        self.body = body

    def pack(self, value=None):
        """Pack a StatsReply using the object's attributes.

        This method will pack the attribute body and body_type before pack the
        StatsReply object, then will return this struct as a binary data.

        Returns:
            stats_reply_packed (bytes): Binary data with StatsReply packed.
        """
        buff = self.body
        if not value:
            value = self.body

        if value and hasattr(value, 'pack'):
            self.body = BinaryData(value.pack())
        stats_reply_packed = super().pack()

        self.body = buff
        return stats_reply_packed

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``body`` attribute which has its type determined
        by the ``body_type`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
        """
        super().unpack(buff[offset:])
        self._unpack_body()

    def _unpack_body(self):
        """Unpack `body` replace it by the result."""
        obj = self._get_body_instance()
        obj.unpack(self.body.value)
        self.body = obj

    def _get_body_instance(self):
        """Method used to return the body instance."""
        pyof_class = self._get_body_class()

        if pyof_class is None:
            return BinaryData(b'')
        elif pyof_class is DescStats:
            return pyof_class()

        return FixedTypeList(pyof_class=pyof_class)

    def _get_body_class(self):
        if isinstance(self.body_type, (int, UBInt16)):
            self.body_type = self.body_type.enum_ref(self.body_type.value)

        body_name = self.body_type.name.replace('OFPST_', '').title()
        module = import_module('pyof.v0x01.controller2switch.common')

        for class_name in module.__all__:
            if 'Request' not in class_name and body_name in class_name:
                return getattr(module, class_name)
        return None
