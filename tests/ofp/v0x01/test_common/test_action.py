import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import action

class TestActionHeader(unittest.TestCase):
    def test_get_size(self):
        action_header = action.ActionHeader()
        self.assertEqual(action_header.get_size(), 8)

    def test_pack(self):
        action_header = action.ActionHeader()
        action_header.pack()

    def test_unpack(self):
        pass

class TestActionOutput(unittest.TestCase):
    def test_get_size(self):
        action_output = action.ActionOutput()
        self.assertEqual(action_output.get_size(), 8)

    def test_pack(self):
        action_output = action.ActionOutput()
        action_output.pack()

    def test_unpack(self):
        pass

class TestActionEnqueue(unittest.TestCase):
    def test_get_size(self):
        action_enqueue = action.ActionEnqueue()
        self.assertEqual(action_enqueue.get_size(), 8)

    def test_pack(self):
        action_enqueue = action.ActionEnqueue()
        action_enqueue.pack()

    def test_unpack(self):
        pass

class TestActionVlanVid(unittest.TestCase):
    def test_get_size(self):
        action_vlan_vid = action.ActionVlanVid()
        self.assertEqual(action_vlan_vid.get_size(), 8)

    def test_pack(self):
        action_vlan_vid = action.ActionVlanVid()
        action_vlan_vid.pack()

    def test_unpack(self):
        pass

class TestActionVlanPCP(unittest.TestCase):
    def test_get_size(self):
        action_vlan_pcp = action.ActionVlanPCP()
        self.assertEqual(action_vlan_pcp.get_size(), 8)

    def test_pack(self):
        action_vlan_pcp = action.ActionVlanPCP()
        action_vlan_pcp.pack()

    def test_unpack(self):
        pass

class TestActionDLAddr(unittest.TestCase):
    def test_get_size(self):
        action_dl_addr = action.ActionDLAddr()
        self.assertEqual(action_dl_addr.get_size(), 8)

    def test_pack(self):
        action_dl_addr = action.ActionDLAddr()
        action_dl_addr.pack()

    def test_unpack(self):
        pass

class TestActionNWAddr(unittest.TestCase):
    def test_get_size(self):
        action_nw_addr = action.ActionNWAddr()
        self.assertEqual(action_nw_addr.get_size(), 8)

    def test_pack(self):
        action_nw_addr = action.ActionNWAddr()
        action_nw_addr.pack()

    def test_unpack(self):
        pass

class TestActionNWTos(unittest.TestCase):
    def test_get_size(self):
        action_nw_tos = action.ActionNWTos()
        self.assertEqual(action_nw_tos.get_size(), 8)

    def test_pack(self):
        action_nw_tos = action.ActionNWTos()
        action_nw_tos.pack()

    def test_unpack(self):
        pass

class TestActionTPPort(unittest.TestCase):
    def test_get_size(self):
        action_tp_port = action.ActionTPPort()
        self.assertEqual(action_tp_port.get_size(), 8)

    def test_pack(self):
        action_tp_port = action.ActionTPPort()
        action_tp_port.pack()

    def test_unpack(self):
        pass

class TestActionVendorHeader(unittest.TestCase):
    def test_get_size(self):
        action_vendor_header = action.ActionVendorHeader()
        self.assertEqual(action_vendor_header.get_size(), 8)

    def test_pack(self):
        action_vendor_header = action.ActionVendorHeader()
        action_vendor_header.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
