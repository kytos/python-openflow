"""Testing Port structures."""
from pyof.v0x01.common.action import (
    ActionDLAddr, ActionEnqueue, ActionNWAddr, ActionNWTos, ActionOutput,
    ActionTPPort, ActionType, ActionVendorHeader, ActionVlanPCP, ActionVlanVid)
from pyof.v0x01.common.phy_port import Port
from tests.test_struct import TestMsgDumpFile


class TestActionOutput(TestMsgDumpFile):
    """ActionOutput message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_output.dat'
    obj = ActionOutput(port=Port.OFPP_CONTROLLER,
                       max_length=8)
    min_size = 8


class TestActionEnqueue(TestMsgDumpFile):
    """ActionEnqueue message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_enqueue.dat'
    obj = ActionEnqueue(port=Port.OFPP_CONTROLLER,
                        queue_id=4)
    min_size = 16


class TestActionVlanVid(TestMsgDumpFile):
    """ActionVlanVid message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_vlan_vid.dat'
    obj = ActionVlanVid(vlan_id=5)
    min_size = 8


class TestActionVlanPCP(TestMsgDumpFile):
    """ActionVlanPCP message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_vlan_pcp.dat'
    obj = ActionVlanPCP(vlan_pcp=2)
    min_size = 8


class TestActionDLAddr(TestMsgDumpFile):
    """ActionDLAddr message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_dl_addr.dat'
    obj = ActionDLAddr(dl_addr_type=ActionType.OFPAT_SET_DL_SRC,
                       dl_addr=[12, 12, 12, 12, 12, 12])
    min_size = 16


class TestActionNWAddr(TestMsgDumpFile):
    """ActionNWAddr message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_nw_addr.dat'
    obj = ActionNWAddr(nw_addr_type=ActionType.OFPAT_SET_NW_SRC,
                       nw_addr=[12, 12, 12, 12, 12, 12])
    min_size = 8


class TestActionNWTos(TestMsgDumpFile):
    """ActionNWTos message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_nw_tos.dat'
    obj = ActionNWTos(nw_tos_type=ActionType.OFPAT_SET_NW_SRC,
                      nw_tos=123456)
    min_size = 8


class TestActionTPPort(TestMsgDumpFile):
    """ActionTPPort message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_tp_port.dat'
    obj = ActionTPPort(tp_port_type=ActionType.OFPAT_SET_TP_SRC,
                       tp_port=8888)
    min_size = 8


class TestActionVendorHeader(TestMsgDumpFile):
    """ActionVendorHeader message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_action_vendor_header.dat'
    obj = ActionVendorHeader(length=16, vendor=1)
    min_size = 8
