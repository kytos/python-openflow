"""group_mod tests."""
from unittest import TestCase

from pyof.v0x04.controller2switch.group_mod import Bucket, GroupMod


class TestGroupMod(TestCase):
    """group_mod tests."""

    def test_min_size(self):
        """Test minimum struct size."""
        self.assertEqual(16, GroupMod().get_size())


class TestBucket(TestCase):
    """bucket tests."""

    def test_min_size(self):
        """Test minimum struct size."""
        self.assertEqual(16, Bucket().get_size())
