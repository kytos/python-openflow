"""Modifications to the port from the controller."""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.common.phy_port import PortConfig, PortFeatures
from pyof.v0x01.foundation.base import GenericMessage
from pyof.v0x01.foundation.basic_types import PAD, HWAddress, UBInt16, UBInt32

__all__ = ('PortMod',)

# Classes


class PortMod(GenericMessage):
    """Implement messages to modify the physical port behavior."""

    header = Header(message_type=Type.OFPT_PORT_MOD)
    port_no = UBInt16()
    hw_addr = HWAddress()
    config = UBInt32(enum_ref=PortConfig)
    mask = UBInt32(enum_ref=PortConfig)
    advertise = UBInt32(enum_ref=PortFeatures)
    #: Pad to 64-bits.
    pad = PAD(4)

    def __init__(self, xid=None, port_no=None, hw_addr=None, config=None,
                 mask=None, advertise=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): OpenFlow xid to the header.
            port_no (int): Physical port number.
            hw_addr (HWAddress): The hardware address is not configurable.
                This is used to sanity-check the request,
                so it must be the same as returned in an ofp_phy_port struct.
            config (PortConfig): Bitmap of OFPPC_* flags
            mask (PortConfig): Bitmap of OFPPC_* flags to be changed
            advertise (PortFeatures): Bitmap of "ofp_port_features"s
        """
        super().__init__(xid)
        self.port_no = port_no
        self.hw_addr = hw_addr
        self.config = config
        self.mask = mask
        self.advertise = advertise
