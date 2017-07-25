"""Test PortMod message."""
from pyof.v0x01.common.phy_port import PortConfig, PortFeatures
from pyof.v0x01.controller2switch.port_mod import PortMod
from tests.test_struct import TestMsgDumpFile


class TestPortMod(TestMsgDumpFile):
    """Test class for PortMod."""

    dumpfile = 'v0x01/ofpt_port_mod.dat'
    obj = PortMod(xid=3, port_no=80,
                  hw_addr='aa:bb:cc:00:33:9f',
                  config=PortConfig.OFPPC_PORT_DOWN,
                  mask=PortConfig.OFPPC_NO_FWD,
                  advertise=PortFeatures.OFPPF_FIBER)
    min_size = 32
