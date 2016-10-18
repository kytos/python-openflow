"""Test for StatsRequest message."""
import unittest

from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.common.utils import unpack_message
from pyof.v0x01.controller2switch.common import PortStatsRequest
from pyof.v0x01.controller2switch.stats_request import StatsRequest, StatsTypes


class TestStatsRequest(unittest.TestCase):
    """Test for StatsRequest message."""

    def setUp(self):
        """Basic test setup."""
        self.message = StatsRequest()
        self.message.header.xid = 1
        self.message.type = StatsTypes.OFPST_FLOW
        self.message.flags = 1
        self.message.body = []

    def test_get_size(self):
        """[Controller2Switch/StatsRequest] - size 12."""
        self.assertEqual(self.message.get_size(), 12)

    def test_pack_unpack_port_stats(self):
        """Pack and unpack PortStatsRequest."""
        body = PortStatsRequest(Port.OFPP_NONE)
        req = StatsRequest(16909060, body_type=StatsTypes.OFPST_PORT,
                           body=body)
        pack = req.pack()
        unpacked = unpack_message(pack)
        self.assertEqual(req, unpacked)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/StatsRequest] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/StatsRequest] - unpacking."""
        # TODO
        pass
