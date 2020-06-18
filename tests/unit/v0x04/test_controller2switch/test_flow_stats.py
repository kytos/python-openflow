"""Flow stats message."""
from pyof.v0x04.common.action import ActionOutput, ListOfActions
from pyof.v0x04.common.flow_instructions import (
    InstructionApplyAction, ListOfInstruction)
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from pyof.v0x04.common.port import PortNo
from pyof.v0x04.controller2switch.common import MultipartType
from pyof.v0x04.controller2switch.multipart_reply import (
    FlowStats, MultipartReply)
from tests.unit.test_struct import TestStruct


class TestFlowStats(TestStruct):
    """Flow stats message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_flow_stats')
        super().set_raw_dump_object(MultipartReply, xid=2898845528,
                                    multipart_type=MultipartType.OFPMP_FLOW,
                                    flags=0,
                                    body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartReply message."""
    return FlowStats(length=88, table_id=0, duration_sec=56,
                     duration_nsec=635000000, priority=1000, idle_timeout=0,
                     hard_timeout=0, flags=0x00000001,
                     cookie=0x0000000000000000, packet_count=18,
                     byte_count=756, match=_new_match(),
                     instructions=_new_list_of_instructions())


def _new_match():
    """Crate new Match instance."""
    oxmtlv1 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                     oxm_field=OxmOfbMatchField.OFPXMT_OFB_ETH_TYPE,
                     oxm_hasmask=False, oxm_value=b'\x88\xcc')
    oxmtlv2 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                     oxm_field=OxmOfbMatchField.OFPXMT_OFB_VLAN_VID,
                     oxm_hasmask=False, oxm_value=b'\x1e\xd7')
    return Match(match_type=MatchType.OFPMT_OXM,
                 oxm_match_fields=[oxmtlv1, oxmtlv2])


def _new_list_of_instructions():
    """Crate new ListOfInstruction."""
    action_output = ActionOutput(port=PortNo.OFPP_CONTROLLER)
    loa = ListOfActions([action_output])
    instruction = InstructionApplyAction(loa)
    return ListOfInstruction([instruction])
