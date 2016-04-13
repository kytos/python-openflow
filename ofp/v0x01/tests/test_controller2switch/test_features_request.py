import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch import features_request


class TestFeaturesRequest(unittest.TestCase):

    def test_get_size(self):
        feature_request = features_request.FeaturesRequest(1)
        self.assertEqual(feature_request.get_size(), 8)

    def test_pack(self):
        feature_request = features_request.FeaturesRequest(1)
        feature_request.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
