import unittest

from pyof.v0x01.common import flow_match
from pyof.v0x01.common import phy_port
from pyof.v0x01.controller2switch import flow_mod


class TestFlowMod(unittest.TestCase):

    def setUp(self):
        self.message = flow_mod.FlowMod()
        self.message.header.xid = 1
        self.message.command = flow_mod.FlowModCommand.OFPFC_ADD
        self.message.match = flow_match.Match()
        self.message.cookie = 0
        self.message.idle_timeout = 300
        self.message.hard_timeout = 6000
        self.message.priority = 1
        self.message.buffer_id = 1
        self.message.out_port = phy_port.Port.OFPP_NONE
        self.message.flags = flow_mod.FlowModFlags.OFPFF_EMERG
        self.message.match.in_port = 80
        self.message.match.dl_src = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_dst = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_vlan = 1
        self.message.match.dl_vlan_pcp = 1
        self.message.match.dl_type = 1
        self.message.match.nw_tos = 1
        self.message.match.nw_proto = 1
        self.message.match.nw_src = 10000
        self.message.match.nw_dst = 10000
        self.message.match.tp_src = 80
        self.message.match.tp_dst = 80

    def test_get_size(self):
        """[Controller2Switch/FlowMod] - size 72"""
        self.assertEqual(self.message.get_size(), 72)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FlowMod] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/FlowMod] - unpacking"""
        # TODO
        pass
