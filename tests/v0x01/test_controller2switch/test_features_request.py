import unittest
import os

from pyof.v0x01.controller2switch import features_request
from pyof.v0x01.common import header as of_header

class TestFeaturesRequest(unittest.TestCase):

    def setUp(self):
        self.message = features_request.FeaturesRequest(1)
        self.head = of_header.Header()

    def test_get_size(self):
        """[Controller2Switch/FeaturesRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FeaturesRequest] - packing"""
        # TODO
        pass

    def test_unpack(self):
        """[Controller2Switch/FeaturesRequest] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_features_request.dat')
        f = open(filename, 'rb')
        self.head.unpack(f.read(8))
        self.assertEqual(self.message.unpack(f.read()), None)
        f.close()
