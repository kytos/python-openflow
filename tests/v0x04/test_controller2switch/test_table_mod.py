"""Table flow modification tests."""
import unittest

from pyof.v0x04.common.header import Type
from pyof.v0x04.controller2switch.table_mod import TableMod


class TestTableMod(unittest.TestCase):
    """TableMod test."""

    def test_min_size(self):
        """Test minimum message size."""
        self.assertEqual(16, TableMod().get_size())

    def test_header_type(self):
        """Test header type."""
        self.assertEqual(Type.OFPT_TABLE_MOD, TableMod().header.message_type)
