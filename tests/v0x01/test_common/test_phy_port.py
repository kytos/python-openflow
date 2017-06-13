"""Testing PhyPort structure."""
from unittest import TestCase, skip

from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x01.common.phy_port import (
    PhyPort, PortConfig, PortFeatures, PortState)


class TestPhyPort(TestCase):
    """Test PhyPort."""

    def setUp(self):
        """Basic setup for test."""
        self.message = PhyPort()
        self.message.port_no = 2
        self.message.hw_addr = '1a:2b:3c:4d:5e:6f'
        self.message.name = bytes('X' * OFP_MAX_PORT_NAME_LEN, 'utf-8')
        self.message.config = PortConfig.OFPPC_NO_STP
        self.message.state = PortState.OFPPS_STP_FORWARD
        self.message.curr = PortFeatures.OFPPF_10GB_FD
        self.message.advertised = PortFeatures.OFPPF_PAUSE
        self.message.supported = PortFeatures.OFPPF_AUTONEG
        self.message.peer = PortFeatures.OFPPF_AUTONEG

    def test_get_size(self):
        """[Common/PhyPort] - size 48."""
        self.assertEqual(self.message.get_size(), 48)

    @skip('Not yet implemented')
    def test_pack(self):
        """[Common/PhyPort] - packing."""
        pass

    @skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PhyPort] - unpacking."""
        pass
