"""Test PortMod message."""
import unittest

from pyof.v0x01.controller2switch import port_mod


class TestPortMod(unittest.TestCase):
    """Test class for PortMod."""

    def setUp(self):
        """Basic test setup."""
        self.message = port_mod.PortMod()
        self.message.header.xid = 1
        self.message.port_no = 80
        self.message.hw_addr = 'aa:bb:cc:00:33:9f'
        self.message.config = 1 << 2
        self.message.mask = 1 << 1
        self.message.advertise = 1

    def test_get_size(self):
        """[Controller2Switch/PortMod] - size 32."""
        self.assertEqual(self.message.get_size(), 32)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/PortMod] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/PortMod] - unpacking."""
        # TODO
        pass
