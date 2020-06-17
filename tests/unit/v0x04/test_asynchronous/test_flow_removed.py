"""Testing v0x04 FlowRemoved message."""
from pyof.v0x04.asynchronous.flow_removed import FlowRemoved, FlowRemovedReason
from pyof.v0x04.common.flow_match import (
    Match, MatchType, OxmClass, OxmOfbMatchField, OxmTLV)
from tests.unit.test_struct import TestStruct


class TestFlowRemovedMsg(TestStruct):
    """FlowRemoved message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_flow_removed')
        super().set_raw_dump_object(FlowRemoved, xid=0,
                                    cookie=0x0000000000000000, priority=1000,
                                    reason=FlowRemovedReason.OFPRR_DELETE,
                                    table_id=0, duration_sec=77,
                                    duration_nsec=559000000, idle_timeout=0,
                                    hard_timeout=0, packet_count=0,
                                    byte_count=0, match=_new_match())
        super().set_minimum_size(56)


def _new_match():
    """Crate new Match instance."""
    tlv1 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                  oxm_field=OxmOfbMatchField.OFPXMT_OFB_ETH_TYPE,
                  oxm_hasmask=False, oxm_value=b'\x88\xcc')
    tlv2 = OxmTLV(oxm_class=OxmClass.OFPXMC_OPENFLOW_BASIC,
                  oxm_field=OxmOfbMatchField.OFPXMT_OFB_VLAN_VID,
                  oxm_hasmask=False, oxm_value=b'\x1e\xd7')
    return Match(match_type=MatchType.OFPMT_OXM,
                 oxm_match_fields=[tlv1, tlv2])
