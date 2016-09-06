"""Table flow tests."""
import unittest

from pyof.v0x04.controller2switch.flow_table import TableMod


class TestTableMod(unittest.TestCase):
    """TableMod test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, TableMod().get_size())
