import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.features_request import FeaturesRequest

class TestFeaturesRequest(unittest.TestCase):
    def test_get_size(self):
        fr = FeaturesRequest(1)
        self.assertEqual(fr.get_size(), 8)

    def test_pack(self):
        fr = FeaturesRequest(1)
        fr.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
