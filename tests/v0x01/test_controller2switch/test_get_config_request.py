import unittest

from pyof.v0x01.controller2switch import get_config_request


class TestGetConfigRequest(unittest.TestCase):

    def setUp(self):
        self.message = get_config_request.GetConfigRequest(1)

    def test_get_size(self):
        """[Controller2Switch/GetConfigRequest] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/GetConfigRequest] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/GetConfigRequest] - unpacking"""
        # TODO
        pass
