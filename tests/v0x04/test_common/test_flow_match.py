"""Testing FlowMatch structure."""
from pyof.v0x04.common import flow_match as fm
from tests.test_struct import TestStructDump


class TestOxmTLV1(TestStructDump):
    dump = b'\x80\x00\x00\x03abc'
    obj = fm.OxmTLV(fm.OxmClass.OFPXMC_OPENFLOW_BASIC,  # class
                    fm.OxmOfbMatchField.OFPXMT_OFB_IN_PORT,  # field
                    0,  # mask
                    b'abc')  # value


class TestOxmTLV2(TestStructDump):
    dump = b'\x80\x00\x00\x02ab'
    obj = fm.OxmTLV(fm.OxmClass.OFPXMC_EXPERIMENTER,
                    2,
                    0,
                    b'de')


class TestOxmTLV3(TestStructDump):
    dump = b'\x80\x00\x00\x04fghi'
    obj = fm.OxmTLV(fm.OxmClass.OFPXMC_OPENFLOW_BASIC,
                    fm.OxmOfbMatchField.OFPXMT_OFB_IN_PHY_PORT,
                    0,
                    b'fghi')


class TestMatch(TestStructDump):
    oxm1_dump = TestOxmTLV1.dump
    oxm2_dump = TestOxmTLV2.dump
    oxm3_dump = TestOxmTLV3.dump

    oxm1_obj = TestOxmTLV1.obj
    oxm2_obj = TestOxmTLV2.obj
    oxm3_obj = TestOxmTLV3.obj

    dump = (b'\x00\x01\x00\x19' +
            oxm1_dump +
            oxm2_dump +
            oxm3_dump)

    obj = fm.Match(
        match_type=fm.MatchType.OFPMT_OXM,
        oxm_match_fields=fm.OxmMatchFields([oxm1_obj,
                                            oxm2_obj,
                                            oxm3_obj]))
