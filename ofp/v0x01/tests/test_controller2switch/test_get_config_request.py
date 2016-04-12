import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from controller2switch.get_config_request import GetConfigRequest

class TestGetConfigRequest(unittest.TestCase):
    def test_get_size(self):
        gcr = GetConfigRequest(1)
        self.assertEqual(gcr.get_size(), 12)

    def test_pack(self):
        gcr = GetConfigRequest(1)
        gcr.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
