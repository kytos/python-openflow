"""FlowMod test."""
import unittest

from pyof.v0x04.controller2switch.flow_mod import FlowMod


class TestFlowMod(unittest.TestCase):
    """FlowMod test."""

    def test_min_size(self):
        """Test struct minimum size."""
        self.assertEqual(56, FlowMod().get_size())
