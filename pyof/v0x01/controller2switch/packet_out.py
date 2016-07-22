"""For the controller to send a packet out through the datapath."""
# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types
from pyof.v0x01.foundation.exceptions import ValidationError

__all__ = ['PacketOut']

# Classes

#: in_port valid virtual port values, for validation
_VIRT_IN_PORTS = (Port.OFPP_LOCAL, Port.OFPP_CONTROLLER, Port.OFPP_NONE)


class PacketOut(base.GenericMessage):
    """Send packet (controller -> datapath).

    Args:
        xid (int): xid of the message header.
        buffer_id (int): ID assigned by datapath (-1 if none).
        in_port (:class:`int`, :class:`.Port`): Packet's input port
            (:attr:`.Port.OFPP_NONE` if none). Virtual ports OFPP_IN_PORT,
            OFPP_TABLE, OFPP_NORMAL, OFPP_FLOOD, and OFPP_ALL cannot be used as
            input port.
        actions_len (int): Size of action array in bytes.
        actions (ListOfActions): Actions (class ActionHeader).
        data (bytes): Packet data. The length is inferred from the length
            field in the header. (Only meaningful if
            buffer_id == -1).
    """

    header = of_header.Header(message_type=of_header.Type.OFPT_PACKET_OUT)
    buffer_id = basic_types.UBInt32()
    in_port = basic_types.UBInt16()
    actions_len = basic_types.UBInt16()
    actions = common.ListOfActions()
    data = basic_types.BinaryData()

    def __init__(self, xid=None, buffer_id=None, in_port=None,
                 actions_len=None, actions=None, data=b''):
        super().__init__()
        self.header.xid = xid
        self.buffer_id = buffer_id
        self.in_port = in_port
        self.actions_len = actions_len
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

    def _validate_in_port(self):
        port = self.in_port
        valid = True
        if isinstance(port, int) and (port < 1 or port >= Port.OFPP_MAX.value):
            valid = False
        elif isinstance(port, Port) and port not in _VIRT_IN_PORTS:
            valid = False
        if not valid:
            raise ValidationError('{} is not a valid input port.'.format(port))
