"""FlowMod test."""
from pyof.v0x04.common.action import ActionOutput, ListOfActions
from pyof.v0x04.common.flow_instructions import (
    InstructionApplyAction, ListOfInstruction)
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.flow_mod import FlowMod, FlowModCommand
from tests.unit.test_struct import TestStruct


class TestFlowMod(TestStruct):
    """FlowMod test."""

    def test_min_size(self):
        """Test struct minimum size."""
        super().set_raw_dump_file('v0x04', 'ofpt_flow_mod')
        super().set_raw_dump_object(FlowMod, xid=2219910763,
                                    command=FlowModCommand.OFPFC_ADD,
                                    priority=1000,
                                    match=_new_match(),
                                    instructions=_new_list_of_instructions())
        super().set_minimum_size(56)


def _new_match():
    """Crate new Match instance."""
    oxm_tlv1 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                      oxm_field=OxmOfbMatchField.OFPXMT_OFB_ETH_TYPE,
                      oxm_hasmask=False, oxm_value=b'\x88\xcc')
    oxmt_lv2 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                      oxm_field=OxmOfbMatchField.OFPXMT_OFB_VLAN_VID,
                      oxm_hasmask=False, oxm_value=b'\x1e\xd7')
    return Match(match_type=MatchType.OFPMT_OXM,
                 oxm_match_fields=[oxm_tlv1, oxmt_lv2])

def _new_list_of_instructions():
    """Crate new ListOfInstruction."""
    output = ActionOutput(port=PortNo.OFPP_CONTROLLER)
    loa = ListOfActions([output])
    instruction = InstructionApplyAction(loa)
    return ListOfInstruction([instruction])
