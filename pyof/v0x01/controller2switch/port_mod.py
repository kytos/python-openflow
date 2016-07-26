"""Modifications to the port from the controller."""

# System imports


# Third-party imports


# Local source tree imports
from pyof.v0x01.common import header as of_header
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

__all__ = ('PortMod')

# Classes


class PortMod(base.GenericMessage):
    """Implement messages to modify the physical port behavior.

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

    header = of_header.Header(message_type=of_header.Type.OFPT_PORT_MOD)
    port_no = basic_types.UBInt16()
    hw_addr = basic_types.HWAddress()
    config = basic_types.UBInt32(enum_ref=phy_port.PortConfig)
    mask = basic_types.UBInt32(enum_ref=phy_port.PortConfig)
    advertise = basic_types.UBInt32(enum_ref=phy_port.PortFeatures)
    #: Pad to 64-bits.
    pad = basic_types.PAD(4)

    def __init__(self, xid=None, port_no=None, hw_addr=None, config=None,
                 mask=None, advertise=None):
        super().__init__()
        self.header.xid = xid if xid else self.header.xid
        self.port_no = port_no
        self.hw_addr = hw_addr
        self.config = config
        self.mask = mask
        self.advertise = advertise
