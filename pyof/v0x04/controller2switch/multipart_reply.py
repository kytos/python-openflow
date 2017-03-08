"""Controller replying state from datapath."""

# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, FixedTypeList, Pad, UBInt16
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.controller2switch.common import MultipartTypes
from pyof.v0x04.common.table_feature import TableFeatures


# Third-party imports


__all__ = ('MultipartReply', 'MultipartReplyFlags')

# Enum


class MultipartReplyFlags(Enum):
    """Flags for MultipartReply."""

    #: More replies to follow.
    OFPMPF_REPLY_MORE = 1 << 0


# Classes


class MultipartReply(GenericMessage):
    """Reply datapath state.

    While the system is running, the controller may reply state from the
    datapath using the OFPT_MULTIPART_REPLY message.
    """

    #: :class:`~.common.header.Header`
    header = Header(message_type=Type.OFPT_MULTIPART_REPLY)
    #: One of the OFPMP_* constants.
    multipart_type = UBInt16(enum_ref=MultipartTypes)
    #: OFPMPF_REPLY_* flags.
    flags = UBInt16(enum_ref=MultipartReplyFlags)
    #: Padding
    pad = Pad(4)
    #: Body of the reply
    body = BinaryData()

    def __init__(self, xid=None, multipart_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to the header.
            multipart_type (int): One of the OFPMP_* constants.
            flags (int): OFPMPF_REPLY_* flags.
            body (bytes): Body of the reply.
        """
        super().__init__(xid)
        self.multipart_type = multipart_type
        self.flags = flags
        self.body = body

    def pack(self, value=None):
        """Pack a StatsReply using the object's attributes.

        This method will pack the attribute body and multipart_type before pack the
        StatsReply object, then will return this struct as a binary data.

        Returns:
            stats_reply_packed (bytes): Binary data with StatsReply packed.
        """
        buff = self.body
        if not value:
            value = self.body
        if value and hasattr(value, 'pack'):
            self.body = BinaryData(value.pack())

        multiparty_packed = super().pack()
        self.body = buff

        return multiparty_packed

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``body`` attribute which has its type determined
        by the ``multipart_type`` attribute.

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
        else:
            return FixedTypeList(pyof_class=pyof_class)

    def _get_body_class(self):
        """Method used to return the body class using the multipart_type."""
        if isinstance(self.multipart_type, (int, UBInt16)):
            self.multipart_type = self.multipart_type.enum_ref(self.multipart_type.value)
        if self.multipart_type.value == 12:
            return TableFeatures
