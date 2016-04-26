import unittest

from ofp.v0x01.asynchronous import port_status
from ofp.v0x01.common import phy_port
from ofp.v0x01.foundation import base


class TestPortStatus(unittest.TestCase):
    """Test the PortStatus message"""

    def setUp(self):
        """Setup the TestPortStatus Class"""
        name = bytes('X' * base.OFP_MAX_PORT_NAME_LEN, 'utf-8')
        self.message = port_status.PortStatus()
        self.message.header.xid = 1
        self.message.reason = port_status.PortReason.OFPPR_ADD
        self.message.pad = [0, 0, 0, 0, 0, 0, 0]
        self.message.desc = phy_port.PhyPort()
        self.message.desc.port_no = 2
        self.message.desc.hw_addr = [10, 10, 18, 18, 16, 16]
        self.message.desc.name = name
        self.message.desc.config = phy_port.OFPPortConfig.OFPPC_NO_STP
        self.message.desc.state = phy_port.OFPPortState.OFPPS_STP_MASK
        self.message.desc.curr = phy_port.OFPPortFeatures.OFPPF_10GB_FD
        self.message.desc.advertised = phy_port.OFPPortFeatures.OFPPF_PAUSE
        self.message.desc.supported = phy_port.OFPPortFeatures.OFPPF_AUTONEG
        self.message.desc.peer = phy_port.OFPPortFeatures.OFPPF_AUTONEG

    def test_size(self):
        """[Asynchronous/PortStatus] - size 64"""
        self.assertEqual(self.message.get_size(), 64)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Asynchronous/PortStatus] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Asynchronous/PortStatus] - unpacking"""
        # TODO
        pass
