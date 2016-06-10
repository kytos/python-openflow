"""When packets are received by the datapath and sent to the controller,
they use the OFPT_PACKET_IN message"""

# System imports
import enum

# Third-party imports

# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Enums


class PacketInReason(enum.Enum):
    """
    Why is this packet being sent to the controller?

        OFPR_NO_MATCH # No matching flow
        OFPR_ACTION   # Action explicitly output to controller

    """
    OFPR_NO_MATCH = 1
    OFPR_ACTION = 2


# Classes


class PacketIn(base.GenericMessage):
    """
    Packet received on port (datapath -> controller)

    :param xid:       Openflow xid of the Header
    :param buffer_id: ID assigned by datapath
    :param total_len: Full length of frame
    :param in_port:   Port on which frame was received
    :param reason:    Reason packet is being sent (one of OFPR_*)
    :param pad:       Align to 32-bits
    :param data:      Ethernet frame, halfway through 32-bit word,
                      so the IP header is 32-bit aligned.  The
                      amount of data is inferred from the length
                      field in the header.  Because of padding,
                      offsetof(struct ofp_packet_in, data) ==
                      sizeof(struct ofp_packet_in) - 2.

    """
    header = of_header.Header(message_type=of_header.Type.OFPT_PACKET_IN)
    buffer_id = basic_types.UBInt32()
    total_len = basic_types.UBInt16()
    in_port = basic_types.UBInt16()
    reason = basic_types.UBInt8(enum_ref=PacketInReason)
    pad = basic_types.PAD(1)
    data = basic_types.BinaryData()

    def __init__(self, xid=None, buffer_id=None, total_len=None, in_port=None,
                 reason=None, data=b''):
        super().__init__()
        self.header.xid = xid
        self.buffer_id = buffer_id
        self.total_len = total_len
        self.in_port = in_port
        self.reason = reason
        self.data = data
