import unittest

from ofp.v0x01.common import phy_port
from ofp.v0x01.foundation import base

class TestPhyPort(unittest.TestCase):
    def setUp(self):
        hw_addr = [100, 50, 48, 48, 160, 160]
        name = bytes("".join(['X' for _ in range(base.OFP_MAX_PORT_NAME_LEN)]),
                     'utf-8')
        self.phy_port = phy_port.PhyPort(port_no=80, hw_addr=hw_addr,
                                         name=name, config=1<<1, state=3<<8,
                                         curr=0, advertised=1<<4,
                                         supported=1<<4, peer=1<<4)

    def test_get_size(self):
        self.assertEqual(self.phy_port.get_size(), 48)

    def test_pack(self):
        self,phy_port.pack()

    def test_unpack(self):
        pass
