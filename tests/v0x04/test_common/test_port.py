"""Test of Port class from common module"""
from unittest import TestCase, skip

from pyof.v0x04.common.port import Port, PortConfig, PortFeatures, PortState


class TestPort(TestCase):

    def setUp(self):
        self.message = Port()
        self.message.port_no = 2
        self.message.hw_addr = '1a:2b:3c:4d:5e:6f'
        self.message.name = 'eth1-s1'
        self.message.config = PortConfig.OFPPC_NO_FWD
        self.message.state = PortState.OFPPS_LIVE
        self.message.curr = PortFeatures.OFPPF_1TB_FD +\
            PortFeatures.OFPPF_FIBER
        self.message.advertised = PortFeatures.OFPPF_PAUSE
        self.message.supported = PortFeatures.OFPPF_AUTONEG
        self.message.peer = PortFeatures.OFPPF_AUTONEG
        self.message.curr_speed = 100
        self.message.max_speed = 1000

    def test_get_size(self):
        """[Common/PhyPort] - size 48"""
        self.assertEqual(self.message.get_size(), 64)

    @skip('Not yet implemented')
    def test_pack(self):
        """[Common/PhyPort] - packing"""
        # TODO
        pass

    @skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PhyPort] - unpacking"""
        # TODO
        pass
