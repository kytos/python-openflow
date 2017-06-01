"""Flow modification (add/delete) message tests."""
from pyof.v0x01.common.action import ActionOutput
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.flow_mod import FlowMod, FlowModCommand
from tests.test_struct import TestStruct


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


def _get_flowmod_kwargs(command):
    """Return parameters for FlowMod object."""
    return {'xid': 4,
            'command': command,
            'match': _get_match(),
            'cookie': 0,
            'idle_timeout': 0,
            'hard_timeout': 0,
            'priority': 32768,
            'buffer_id': 4294967295,
            'out_port': Port.OFPP_NONE,
            'flags': 0,
            'actions': _get_actions()}


def _get_match():
    """Return a Match object."""
    return Match()


def _get_actions():
    """Return a List of actions registered by flow object."""
    action = ActionOutput(port=65533, max_length=65535)
    return [action]
