"""Test for PortStatsRequest."""
import unittest

from pyof.v0x01.controller2switch.common import PortStatsRequest


class TestPortStatsRequest(unittest.TestCase):
    """Test for PortStatsRequest."""

    def setUp(self):
        """Basic test setup."""
        self.message = PortStatsRequest()
        self.message.port_no = 80

    def test_get_size(self):
        """[Controller2Switch/PortStatsRequest] - size 8."""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/PortStatsRequest] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/PortStatsRequest] - unpacking."""
        # TODO
        pass
