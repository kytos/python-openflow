"""Flow modification (add/delete) message tests."""
from pyof.v0x01.common.action import ActionOutput
from pyof.v0x01.common.flow_match import Match
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch.flow_mod import FlowMod, FlowModCommand
from tests.test_struct import TestMsgDumpFile


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


class TestFlowAdd(TestMsgDumpFile):
    """Flow addition message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_flow_add.dat'
    kwargs = _get_flowmod_kwargs(FlowModCommand.OFPFC_ADD)
    obj = FlowMod(**kwargs)
    min_size = 72


class TestFlowDelete(TestMsgDumpFile):
    """Flow deletion message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_flow_delete.dat'
    kwargs = _get_flowmod_kwargs(FlowModCommand.OFPFC_DELETE)
    obj = FlowMod(**kwargs)
