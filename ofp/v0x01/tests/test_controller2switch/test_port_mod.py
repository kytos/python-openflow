import unittest

from ofp.v0x01.common import header
from ofp.v0x01.controller2switch import port_mod
from ofp.v0x01.foundation import base


class TestPortMod(unittest.TestCase):

    def test_get_size(self):
        ofp_header = header.OFPHeader(1, 40, 1)
        hw_addr=[1 for _ in range(base.OFP_ETH_ALEN)]
        port_mod_message = port_mod.PortMod(header=ofp_header, port_no=80,
                                            hw_addr=hw_addr, config=1 << 2,
                                            mask=1 << 1, advertise=1,
                                            pad=[0, 0, 0, 0])
        self.assertEqual(port_mod_message.get_size(), 32)

    def test_pack(self):
        ofp_header = header.OFPHeader(1, 40, 1)
        hw_addr=[1 for _ in range(base.OFP_ETH_ALEN)]
        port_mod_message = port_mod.PortMod(header=ofp_header, port_no=80,
                                            hw_addr=hw_addr, config=1 << 2,
                                            mask=1 << 1, advertise=1,
                                            pad=[0, 0, 0, 0])
        port_mod_message.pack()

    def test_unpack(self):
        pass
