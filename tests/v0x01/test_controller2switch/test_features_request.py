import unittest

from ofp.v0x01.controller2switch import features_request

class TestFeaturesRequest(unittest.TestCase):

    def setUp(self):
        self.message = features_request.FeaturesRequest(1)

    def test_get_size(self):
        """[Controller2Switch/FeaturesRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FeaturesRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/FeaturesRequest] - unpacking"""
        # TODO
        pass
