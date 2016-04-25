import unittest

from ofp.v0x01.controller2switch import port_stats_request as PSR


class TestPortStatsRequest(unittest.TestCase):
    def setUp(self):
        self.message = PSR.PortStatsRequest(port_no=80, pad=[0, 0, 0, 0, 0, 0])

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 8)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
