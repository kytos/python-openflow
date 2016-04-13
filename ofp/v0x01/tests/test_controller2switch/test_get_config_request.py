import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch import get_config_request


class TestGetConfigRequest(unittest.TestCase):

    def test_get_size(self):
        get_config_request_message = get_config_request.GetConfigRequest(1)
        self.assertEqual(get_config_request_message.get_size(), 12)

    def test_pack(self):
        get_config_request_message = get_config_request.GetConfigRequest(1)
        get_config_request_message.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
