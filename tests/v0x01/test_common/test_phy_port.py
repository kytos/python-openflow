import unittest

from pyof.v0x01.common import phy_port
from pyof.v0x01.foundation import base


class TestPhyPort(unittest.TestCase):

    def setUp(self):
        self.message = phy_port.PhyPort()
        self.message.port_no = 2
        self.message.hw_addr = '1a:2b:3c:4d:5e:6f'
        self.message.name = bytes('X' * base.OFP_MAX_PORT_NAME_LEN, 'utf-8')
        self.message.config = phy_port.PortConfig.OFPPC_NO_STP
        self.message.state = phy_port.PortState.OFPPS_STP_FORWARD
        self.message.curr = phy_port.PortFeatures.OFPPF_10GB_FD
        self.message.advertised = phy_port.PortFeatures.OFPPF_PAUSE
        self.message.supported = phy_port.PortFeatures.OFPPF_AUTONEG
        self.message.peer = phy_port.PortFeatures.OFPPF_AUTONEG

    def test_get_size(self):
        """[Common/PhyPort] - size 48"""
        self.assertEqual(self.message.get_size(), 48)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/PhyPort] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PhyPort] - unpacking"""
        # TODO
        pass
