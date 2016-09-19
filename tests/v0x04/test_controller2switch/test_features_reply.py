"""FeturesReply test."""
import unittest

from pyof.v0x04.controller2switch.features_reply import FeaturesReply


class TestFeaturesReply(unittest.TestCase):
    """FeaturesReply test."""

    def test_min_size(self):
        """Test struct minimum size."""
        self.assertEqual(32, FeaturesReply().get_size())
