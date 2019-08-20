"""Testing PhyPort structure."""
import os
from unittest import TestCase

from pyof.foundation.basic_types import HWAddress
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x01.common.phy_port import (
    PhyPort, PortConfig, PortFeatures, PortState)


class TestPhyPort(TestCase):
    """Test PhyPort."""

    def setUp(self):
        """Basic setup for test."""
        self.message = PhyPort()
        self.message.port_no = 1
        self.message.hw_addr = HWAddress('9a:da:11:8a:f4:0c')
        self.message.name = 's1-eth1'
        self.message.state = PortState.OFPPS_STP_LISTEN
        self.message.curr = (PortFeatures.OFPPF_10GB_FD |
                             PortFeatures.OFPPF_COPPER)

    def test_get_size(self):
        """[Common/PhyPort] - size 48."""
        self.assertEqual(self.message.get_size(), 48)
    
    def test_pack(self):
        """[Common/PhyPort] - packing."""
        data = b'\x00\x01\x9a\xda\x11\x8a\xf4\x0cs1-eth1\x00\x00\x00\x00\x00'
        data += 15 * b'\x00'
        data += b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(self.message.pack(), data)

    def test_unpack(self):
        """[Common/PhyPort] - unpacking."""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_port_status.dat')
        f = open(filename, 'rb')
        f.seek(16, 1)
        self.message.unpack(f.read(48))

        self.assertEqual(self.message.port_no, 1)
        self.assertEqual(self.message.hw_addr, '9a:da:11:8a:f4:0c')
        self.assertEqual(self.message.name, 's1-eth1')
        self.assertEqual(self.message.state, PortState.OFPPS_STP_LISTEN)
        self.assertEqual(self.message.curr, (PortFeatures.OFPPF_10GB_FD |
                                             PortFeatures.OFPPF_COPPER))

        f.close()
