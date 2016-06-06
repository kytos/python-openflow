import unittest

from pyof.v0x01.common import action
from pyof.v0x01.common import phy_port


class TestActionHeader(unittest.TestCase):
    """Test the ActionHeader message"""

    def setUp(self):
        self.message = action.ActionHeader()
        self.message.action_type = action.ActionType.OFPAT_SET_TP_SRC
        self.message.len = 1

    def test_get_size(self):
        """[Common/ActionHeader] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionHeader] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionHeader] - unpacking"""
        # TODO
        pass


class TestActionOutput(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionOutput()
        self.message.port = phy_port.Port.OFPP_CONTROLLER
        self.message.max_len = 8

    def test_get_size(self):
        """[Common/ActionOutput] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionOutput] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionOutput] - packing"""
        # TODO
        pass


class TestActionEnqueue(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionEnqueue()
        self.message.port = phy_port.Port.OFPP_CONTROLLER
        self.message.queue_id = 4

    def test_get_size(self):
        """[Common/ActionEnqueue] - size 16"""
        self.assertEqual(self.message.get_size(), 16)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionEnqueue] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionEnqueue] - unpacking"""
        # TODO
        pass


class TestActionVlanVid(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionVlanVid()
        self.message.length = 2
        self.message.vlan_vid = 5

    def test_get_size(self):
        """[Common/ActionVlanVid] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionVlanVid] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionVlanVid] - unpacking"""
        # TODO


class TestActionVlanPCP(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionVlanPCP()
        self.message.vlan_pcp = 2

    def test_get_size(self):
        """[Common/ActionVlanPCP] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/Actionvlanpcp] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionVlanVid] - unpacking"""
        # TODO


class TestActionDLAddr(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionDLAddr()
        self.message.dl_addr_type = action.ActionType.OFPAT_SET_DL_SRC
        self.message.dl_addr = [12, 12, 12, 12, 12, 12]

    def test_get_size(self):
        """[Common/ActionDLAddr] - size 16"""
        self.assertEqual(self.message.get_size(), 16)


    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionDLAddr] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionDLAddr] - unpacking"""
        # TODO


class TestActionNWAddr(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionNWAddr()
        self.message.nw_addr_type = action.ActionType.OFPAT_SET_NW_SRC
        self.message.nw_addr = [12, 12, 12, 12, 12, 12]

    def test_get_size(self):
        """[Common/ActionNWAddr] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionNWAddr] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionNWAddr] - unpacking"""
        # TODO


class TestActionNWTos(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionNWTos()
        self.message.nw_tos_type = action.ActionType.OFPAT_SET_NW_SRC
        self.message.nw_tos = 123456

    def test_get_size(self):
        """[Common/ActionNWTos] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionNWTos] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionNWTos] - unpacking"""
        # TODO


class TestActionTPPort(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionTPPort()
        self.message.tp_port_type = action.ActionType.OFPAT_SET_TP_SRC
        self.message.tp_port = 8888

    def test_get_size(self):
        """[Common/ActionTPPort] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionTPPort] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionTPPort] - unpacking"""
        # TODO


class TestActionVendorHeader(unittest.TestCase):

    def setUp(self):
        self.message = action.ActionVendorHeader()
        self.message.length = 16
        self.message.vendor = 1

    def test_get_size(self):
        """[Common/ActionVendorHeader] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/ActionVendorHeader] - packing"""
        # TODO

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/ActionVendorHeader] - unpacking"""
        # TODO
