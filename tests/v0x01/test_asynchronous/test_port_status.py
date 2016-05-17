import unittest

from pyof.v0x01.asynchronous import port_status
from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base


class TestPortStatus(unittest.TestCase):
    """Test the PortStatus message"""

    def setUp(self):
        """Setup the TestPortStatus Class"""
        name = bytes('X' * base.OFP_MAX_PORT_NAME_LEN, 'utf-8')
        self.message = port_status.PortStatus()
        self.message.header.xid = 1
        self.message.reason = port_status.PortReason.OFPPR_ADD
        self.message.desc = phy_port.PhyPort()
        self.message.desc.port_no = 2
        self.message.desc.hw_addr = [10, 10, 18, 18, 16, 16]
        self.message.desc.name = name
        self.message.desc.config = phy_port.PortConfig.OFPPC_NO_STP
        self.message.desc.state = phy_port.PortState.OFPPS_STP_FORWARD
        self.message.desc.curr = phy_port.PortFeatures.OFPPF_10GB_FD
        self.message.desc.advertised = phy_port.PortFeatures.OFPPF_PAUSE
        self.message.desc.supported = phy_port.PortFeatures.OFPPF_AUTONEG
        self.message.desc.peer = phy_port.PortFeatures.OFPPF_AUTONEG

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
