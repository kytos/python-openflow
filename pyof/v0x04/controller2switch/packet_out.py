"""For the controller to send a packet out through the datapath."""
from copy import deepcopy

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, Pad, UBInt16, UBInt32
from pyof.foundation.exceptions import PackException, ValidationError
from pyof.v0x04.common.action import ListOfActions
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import Port, PortNo

__all__ = ('PacketOut',)

# Classes

#: in_port valid virtual port values, for validation
_VIRT_IN_PORTS = (PortNo.OFPP_LOCAL, PortNo.OFPP_CONTROLLER, PortNo.OFPP_ANY)


class PacketOut(GenericMessage):
    """Send packet (controller -> datapath)."""

    #: Openflow :class:`~pyof.v0x04.common.header.Header`
    header = Header(message_type=Type.OFPT_PACKET_OUT)
    #: ID assigned by datapath (OFP_NO_BUFFER if none).
    buffer_id = UBInt32()
    #: Packet’s input port or OFPP_CONTROLLER.
    #: TODO: This field have a enum_ref ?
    in_port = UBInt32(enum_ref=PortNo)
    #: Size of action array in bytes.
    actions_len = UBInt16()
    #: Padding
    pad = Pad(6)
    #: Action List.
    actions = ListOfActions()
    #: Packet data. The length is inferred from the length field in the header.
    #:    (Only meaningful if buffer_id == -1.)
    data = BinaryData()

    def __init__(self, xid=None, buffer_id=None, in_port=None, actions=None,
                 data=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid of the message header.
            buffer_id (int): ID assigned by datapath (-1 if none).
            in_port (:class:`int`, :class:`~pyof.v0x04.common.port.Port`):
                Packet's input port (:attr:`Port.OFPP_NONE` if none).
                Virtual ports OFPP_IN_PORT, OFPP_TABLE, OFPP_NORMAL,
                OFPP_FLOOD, and OFPP_ALL cannot be used as input port.
            actions (ListOfActions): Actions (class ActionHeader).
            data (bytes): Packet data. The length is inferred from the length
                field in the header. (Only meaningful if ``buffer_id`` == -1).
        """
        super().__init__(xid)
        self.buffer_id = buffer_id
        self.in_port = in_port
        self.actions = [] if actions is None else actions
        self.data = data

    def validate(self):
        """Validate the entire message."""
        if not super().is_valid():
            raise ValidationError()
        self._validate_in_port()

    def is_valid(self):
        """Answer if this message is valid."""
        try:
            self.validate()
            return True
        except ValidationError:
            return False

    def pack(self, value=None):
        """Update the action_len attribute and call super's pack."""
        if value is None:
            self._update_actions_len()
            return super().pack()
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``actions`` attribute which has a length determined
        by the ``actions_len`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for attribute_name, class_attribute in self.get_class_attributes():
            if type(class_attribute).__name__ != "Header":
                attribute = deepcopy(class_attribute)
                if attribute_name == 'actions':
                    length = self.actions_len.value
                    attribute.unpack(buff[begin:begin+length])
                else:
                    attribute.unpack(buff, begin)
                setattr(self, attribute_name, attribute)
                begin += attribute.get_size()

    def _update_actions_len(self):
        """Update the actions_len field based on actions value."""
        if isinstance(self.actions, ListOfActions):
            self.actions_len = self.actions.get_size()
        else:
            self.actions_len = ListOfActions(self.actions).get_size()

    def _validate_in_port(self):
        port = self.in_port
        valid = True
        if isinstance(port, int) and (port < 1 or
                                      port >= PortNo.OFPP_MAX.value):
            valid = False
        elif isinstance(port, Port) and port not in _VIRT_IN_PORTS:
            valid = False
        if not valid:
            raise ValidationError('{} is not a valid input port.'.format(port))
