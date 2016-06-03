"""When the controller wishes to send a packet out through the datapath, it
uses the OFPT_PACKET_OUT message"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.controller2switch import common
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Classes


class PacketOut(base.GenericMessage):
    """
    Send packet (controller -> datapath)

        :param xid:         xid of the message header
        :param buffer_id:   ID assigned by datapath (-1 if none)
        :param in_port:     Packet's input port (OFPP_NONE if none).
                            Virtual ports OFPP_IN_PORT, OFPP_TABLE,
                            OFPP_NORMAL, OFPP_FLOOD, and OFPP_ALL cannot be
                            used as an input port.
        :param actions_len: Size of action array in bytes
        :param actions:     Actions (class ActionHeader)
        :param data:        Packet data. The length is inferred from the length
                            field in the header. (Only meaningful if
                            buffer_id == -1.)
    """
    header = of_header.Header()
    buffer_id = basic_types.UBInt32()
    in_port = basic_types.UBInt16()
    actions_len = basic_types.UBInt16()
    actions = common.ListOfActions()
    data = basic_types.BinaryData()

    def __init__(self, xid=None, buffer_id=None, in_port=None,
                 actions_len=None, actions=None, data=b''):
        self.header.xid = xid
        self.header.message_type = of_header.Type.OFPT_PACKET_OUT
        self.buffer_id = buffer_id
        self.in_port = in_port
        self.actions_len = actions_len
        self.actions = [] if actions is None else actions
        self.data = data
