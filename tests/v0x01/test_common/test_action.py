"""Testing Port structures."""
from pyof.v0x01.common.action import (
    ActionDLAddr, ActionEnqueue, ActionNWAddr, ActionNWTos, ActionOutput,
    ActionTPPort, ActionType, ActionVendorHeader, ActionVlanPCP, ActionVlanVid)
from pyof.v0x01.common.phy_port import Port
from tests.test_struct import TestStruct


class TestActionOutput(TestStruct):
    """ActionOutput message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_output')
        super().set_raw_dump_object(ActionOutput, port=Port.OFPP_CONTROLLER,
                                    max_length=8)
        super().set_minimum_size(8)


class TestActionEnqueue(TestStruct):
    """ActionEnqueue message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_enqueue')
        super().set_raw_dump_object(ActionEnqueue, port=Port.OFPP_CONTROLLER,
                                    queue_id=4)
        super().set_minimum_size(16)


class TestActionVlanVid(TestStruct):
    """ActionVlanVid message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_vlan_vid')
        super().set_raw_dump_object(ActionVlanVid, vlan_id=5)
        super().set_minimum_size(8)


class TestActionVlanPCP(TestStruct):
    """ActionVlanPCP message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_vlan_pcp')
        super().set_raw_dump_object(ActionVlanPCP, vlan_pcp=2)
        super().set_minimum_size(8)


class TestActionDLAddr(TestStruct):
    """ActionDLAddr message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_dl_addr')
        super().set_raw_dump_object(ActionDLAddr,
                                    dl_addr_type=ActionType.OFPAT_SET_DL_SRC,
                                    dl_addr=[12, 12, 12, 12, 12, 12])
        super().set_minimum_size(16)


class TestActionNWAddr(TestStruct):
    """ActionNWAddr message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_nw_addr')
        super().set_raw_dump_object(ActionNWAddr,
                                    nw_addr_type=ActionType.OFPAT_SET_NW_SRC,
                                    nw_addr=[12, 12, 12, 12, 12, 12])
        super().set_minimum_size(8)


class TestActionNWTos(TestStruct):
    """ActionNWTos message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_nw_tos')
        super().set_raw_dump_object(ActionNWTos,
                                    nw_tos_type=ActionType.OFPAT_SET_NW_SRC,
                                    nw_tos=123456)
        super().set_minimum_size(8)


class TestActionTPPort(TestStruct):
    """ActionTPPort message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_tp_port')
        super().set_raw_dump_object(ActionTPPort,
                                    tp_port_type=ActionType.OFPAT_SET_TP_SRC,
                                    tp_port=8888)
        super().set_minimum_size(8)


class TestActionVendorHeader(TestStruct):
    """ActionVendorHeader message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_action_vendor_header')
        super().set_raw_dump_object(ActionVendorHeader, length=16, vendor=1)
        super().set_minimum_size(8)
