"""Testing FlowMatch structure."""
from pyof.foundation.basic_types import HWAddress, IPAddress
from pyof.v0x01.common.flow_match import Match
from tests.test_struct import TestStructDump


class TestMatch(TestStructDump):
    """Test Match structure."""

    dump = b'\x00\x0f\xff\x00\x00\x16\x01\x02\x03\x04\x05\x06\x01\x02\x03\x04'
    dump += b'\x05\x06\x00\x01\x01\x00\x00\x01\x01\x01\x00\x00\xc0\xa8\x00\x01'
    dump += b'\xc0\xa8\x00\x02\x00\x16\x00\x16'  # needs to be checked
    obj = Match(in_port=22,
                dl_src=[1, 2, 3, 4, 5, 6],
                dl_dst=[1, 2, 3, 4, 5, 6],
                dl_vlan=1,
                dl_vlan_pcp=1,
                dl_type=1,
                nw_tos=1,
                nw_proto=1,
                nw_src=[192, 168, 0, 1],
                nw_dst=[192, 168, 0, 2],
                tp_src=22,
                tp_dst=22)


class TestMatch2(TestStructDump):
    """Test Match structure."""

    dump = b'\x00\x0f\xff\x0c\x00P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    dump += b'\x00\x00\x00\x01\x01\x00\x00\x01\x01\x01\x00\x00\xc0\xa8\x00'
    dump += b'\x01\xc0\xa8\x00\x02\x00P\x00P'
    obj = Match(in_port=80, dl_vlan=1, dl_vlan_pcp=1, dl_type=1,
                nw_tos=1, nw_proto=1, tp_src=80, tp_dst=80,
                dl_src=HWAddress('00:00:00:00:00:00'),
                dl_dst=HWAddress('00:00:00:00:00:00'),
                nw_src=IPAddress('192.168.0.1'),
                nw_dst=IPAddress('192.168.0.2'))
