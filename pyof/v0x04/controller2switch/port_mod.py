"""Modifications to the port from the controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import HWAddress, Pad, UBInt32
from pyof.v0x04.common.header import Header, Type
from pyof.v0x04.common.port import PortConfig, PortFeatures

__all__ = ('PortMod',)

# Classes


class PortMod(GenericMessage):
    """Implement messages to modify the physical port behavior."""

    header = Header(message_type=Type.OFPT_PORT_MOD)
    port_no = UBInt32()
    pad = Pad(4)
    hw_addr = HWAddress()
    pad2 = Pad(2)
    config = UBInt32(enum_ref=PortConfig)
    mask = UBInt32(enum_ref=PortConfig)
    advertise = UBInt32(enum_ref=PortFeatures)
    #: Pad to 64-bits.
    pad3 = Pad(4)

    def __init__(self, xid=None, port_no=None, hw_addr=None, config=None,
                 mask=None, advertise=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): OpenFlow xid to the header.
            port_no (int): Physical port number.
            hw_addr (HWAddress): The hardware address is not configurable.
                This is used to sanity-check the request,
                so it must be the same as returned in an ofp_phy_port struct.
            config (~pyof.v0x04.common.port.PortConfig):
                Bitmap of OFPPC_* flags
            mask (~pyof.v0x04.common.port.PortConfig):
                Bitmap of OFPPC_* flags to be changed
            advertise (~pyof.v0x04.common.port.PortFeatures):
                Bitmap of OFPPF_*. Zero all bits to prevent any action taking
                place.
        """
        super().__init__(xid)
        self.port_no = port_no
        self.hw_addr = hw_addr
        self.config = config
        self.mask = mask
        self.advertise = advertise
