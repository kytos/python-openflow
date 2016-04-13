import unittest

from ofp.v0x01.controller2switch import port_mod
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class TestPortMod(unittest.TestCase):

    def test_get_size(self):
        port_mod_message = port_mod.PortMod(port_no=80,
                                            hw_addr=basic_types.UBInt8Array(
                                                value=123000,
                                                length=base.OFP_ETH_ALEN),
                                            config=1 << 2, mask=1 << 1,
                                            advertise=1)
        self.assertEqual(port_mod_message.get_size(), 32)

    def test_pack(self):
        port_mod_message = port_mod.PortMod(port_no=80,
                                            hw_addr=basic_types.UBInt8Array(
                                                value=123000,
                                                length=base.OFP_ETH_ALEN),
                                            config=1 << 2, mask=1 << 1,
                                            advertise=1)
        port_mod_message.pack()

    def test_unpack(self):
        pass
