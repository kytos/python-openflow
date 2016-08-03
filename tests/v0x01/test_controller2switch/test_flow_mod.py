"""Flow modification (add/delete) message tests."""
import unittest

from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.flow_mod import (FlowMod, FlowModCommand,
                                                   FlowModFlags)
from tests.teststruct import TestStruct


class TestFlowAdd(TestStruct):
    """Flow addition message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_flow_add')
        kwargs = _get_flowmod_kwargs(FlowModCommand.OFPFC_ADD)
        super().set_raw_dump_object(FlowMod, **kwargs)
        super().set_minimum_size(72)

    @unittest.skip('Need to recover dump contents.')
    def test_pack(self):
        pass

    @unittest.skip('Need to recover dump contents.')
    def test_unpack(self):
        pass


class TestFlowDelete(TestStruct):
    """Flow deletion message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_flow_delete')
        kwargs = _get_flowmod_kwargs(FlowModCommand.OFPFC_DELETE)
        super().set_raw_dump_object(FlowMod, **kwargs)
        # No need to test minimum size again.

    @unittest.skip('Need to recover dump contents.')
    def test_pack(self):
        pass

    @unittest.skip('Need to recover dump contents.')
    def test_unpack(self):
        pass


def _get_flowmod_kwargs(command):
    """Return parameters for FlowMod object."""
    return {'xid': 1,
            'command': command,
            'match': _get_match(),
            'cookie': 0,
            'idle_timeout': 300,
            'hard_timeout': 6000,
            'priority': 1,
            'buffer_id': 1,
            'out_port': Port.OFPP_NONE,
            'flags': FlowModFlags.OFPFF_EMERG}


def _get_match():
    """Return a Match object."""
    return Match(wildcards=0, in_port=80, dl_src='1a:2b:3c:4d:5e:6f',
                 dl_dst='6a:5b:4c:43:2e:1f', dl_vlan=1, dl_vlan_pcp=1,
                 dl_type=1, nw_tos=1, nw_proto=1, nw_src=10000,
                 nw_dst=10000, tp_src=80, tp_dst=80)
