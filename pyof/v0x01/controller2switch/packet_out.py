"""For the controller to send a packet out through the datapath."""
from copy import deepcopy

from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, UBInt16, UBInt32
from pyof.foundation.exceptions import PackException, ValidationError
from pyof.v0x01.common.action import ListOfActions
from pyof.v0x01.common.constants import NO_BUFFER
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import Port

__all__ = ('PacketOut',)

# Classes

#: in_port valid virtual port values, for validation
_VIRT_IN_PORTS = (Port.OFPP_LOCAL, Port.OFPP_CONTROLLER, Port.OFPP_NONE)


class PacketOut(GenericMessage):
    """Send packet (controller -> datapath)."""

    #: :class:`~pyof.v0x01.common.header.Header`
    header = Header(message_type=Type.OFPT_PACKET_OUT)
    buffer_id = UBInt32()
    in_port = UBInt16()
    actions_len = UBInt16()
    actions = ListOfActions()
    data = BinaryData()

    def __init__(self, xid=None, buffer_id=NO_BUFFER, in_port=Port.OFPP_NONE,
                 actions=None, data=b''):
        """Create a PacketOut with the optional parameters below.

        Args:
            xid (int): xid of the message header.
            buffer_id (int): ID assigned by datapath (-1 if none).
            in_port (:class:`int` / :class:`~pyof.v0x01.common.phy_port.Port`):
                Packet's input port (:attr:`.Port.OFPP_NONE` if none). Virtual
                ports :attr:`Port.OFPP_IN_PORT`, :attr:`Port.OFPP_TABLE`,
                :attr:`Port.OFPP_NORMAL`, :attr:`Port.OFPP_FLOOD`, and
                :attr:`Port.OFPP_ALL` cannot be used as input port.
            actions (~pyof.v0x01.common.action.ListOfActions): List of Actions.
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
        """Validate in_port attribute.

        A valid port is either:

            * Greater than 0 and less than or equals to Port.OFPP_MAX
            * One of the valid virtual ports: Port.OFPP_LOCAL,
              Port.OFPP_CONTROLLER or Port.OFPP_NONE

        Raises:
            ValidationError: If in_port is an invalid port.

        """
        is_valid_range = self.in_port > 0 and self.in_port <= Port.OFPP_MAX
        is_valid_virtual_in_ports = self.in_port in _VIRT_IN_PORTS

        if (is_valid_range or is_valid_virtual_in_ports) is False:
            raise ValidationError(f'{self.in_port} is not a valid input port.')
