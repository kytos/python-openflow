"""MultipartReply message test."""

from pyof.foundation.basic_types import HWAddress
from pyof.v0x04.common.port import (
    ListOfPorts, Port, PortConfig, PortFeatures, PortNo, PortState)
from pyof.v0x04.controller2switch.common import MultipartType
from pyof.v0x04.controller2switch.multipart_reply import MultipartReply
from tests.test_struct import TestStruct


class TestPortDesc(TestStruct):
    """Test PortDesc."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        mp_type = MultipartType.OFPMP_PORT_DESC
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_port_desc')
        super().set_raw_dump_object(MultipartReply, xid=1917225664,
                                    multipart_type=mp_type,
                                    flags=0,
                                    body=_get_body())
        super().set_minimum_size(16)


def _get_body():
    """Return the body used by MultipartReply message."""
    port1 = Port(port_no=PortNo.OFPP_LOCAL,
                 hw_addr=HWAddress('5a:ee:a5:a0:62:4f'),
                 name='s1',
                 config=PortConfig.OFPPC_PORT_DOWN,
                 state=PortState.OFPPS_LINK_DOWN,
                 curr=0,
                 advertised=0,
                 supported=0,
                 peer=0,
                 curr_speed=0,
                 max_speed=0)
    port2 = Port(port_no=1,
                 hw_addr=HWAddress('4e:bf:ca:27:8e:ca'),
                 name='s1-eth1',
                 config=0,
                 state=PortState.OFPPS_LIVE,
                 curr=PortFeatures.OFPPF_10GB_FD | PortFeatures.OFPPF_COPPER,
                 advertised=0,
                 supported=0,
                 peer=0,
                 curr_speed=10000000,
                 max_speed=0)
    port3 = Port(port_no=2,
                 hw_addr=HWAddress('26:1f:b9:5e:3c:c7'),
                 name='s1-eth2',
                 config=0,
                 state=PortState.OFPPS_LIVE,
                 curr=PortFeatures.OFPPF_10GB_FD | PortFeatures.OFPPF_COPPER,
                 advertised=0,
                 supported=0,
                 peer=0,
                 curr_speed=10000000,
                 max_speed=0)
    lop = ListOfPorts([port1, port2, port3])
    return lop
