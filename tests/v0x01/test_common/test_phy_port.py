"""Testing PhyPort structure."""
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x01.common.phy_port import (
    PhyPort, PortConfig, PortFeatures, PortState)
from tests.test_struct import TestStructDump


class TestPhyPort(TestStructDump):
    """Test PhyPort class."""

    dump = b'\x00\x02\x1a+<M^oXXXXXXXXXXXXXXX\x00\x00\x00\x00\x02\x00\x00\x02'
    dump += b'\x00\x00\x00\x00@\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x02'
    dump += b'\x00'

    obj = PhyPort(port_no=2,
                  hw_addr='1a:2b:3c:4d:5e:6f',
                  name='X' * OFP_MAX_PORT_NAME_LEN,
                  config=PortConfig.OFPPC_NO_STP,
                  state=PortState.OFPPS_STP_FORWARD,
                  curr=PortFeatures.OFPPF_10GB_FD,
                  advertised=PortFeatures.OFPPF_PAUSE,
                  supported=PortFeatures.OFPPF_AUTONEG,
                  peer=PortFeatures.OFPPF_AUTONEG)
