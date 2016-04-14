import unittest

from ofp.v0x01.controller2switch import port_mod
from ofp.v0x01.foundation import base


class TestPortMod(unittest.TestCase):

    def test_get_size(self):
        hw_addr=[1 for _ in range(base.OFP_ETH_ALEN)]
        port_mod_message = port_mod.PortMod(port_no=80,
                                            hw_addr=hw_addr,
                                            config=1 << 2, mask=1 << 1,
                                            advertise=1)
        self.assertEqual(port_mod_message.get_size(), 32)

    def test_pack(self):
        hw_addr=[1 for _ in range(base.OFP_ETH_ALEN)]
        port_mod_message = port_mod.PortMod(port_no=80,
                                            hw_addr=hw_addr,
                                            config=1 << 2, mask=1 << 1,
                                            advertise=1)
        port_mod_message.pack()

    def test_unpack(self):
        pass
