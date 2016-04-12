import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.port_mod import PortMod
from foundation.base import OFP_ETH_ALEN
from foundation.basic_types import UBInt8Array

class TestPortMod(unittest.TestCase):
    def test_get_size(self):
        pm = PortMod(port_no=80,
                     hw_addr=UBInt8Array(value=123000, length=OFP_ETH_ALEN),
                     config=1<<2, mask=1<<1, advertise=1)
        self.assertEqual(pm.get_size(), 32)

    def test_pack(self):
        pm = PortMod(port_no=80,
                     hw_addr=UBInt8Array(value=123000, length=OFP_ETH_ALEN),
                     config=1<<2, mask=1<<1, advertise=1)
        pm.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
