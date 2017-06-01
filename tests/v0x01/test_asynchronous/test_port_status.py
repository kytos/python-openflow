"""Port Status message tests."""
from pyof.foundation.basic_types import HWAddress
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x01.asynchronous.port_status import PortReason, PortStatus
from pyof.v0x01.common.phy_port import (
    PhyPort, PortConfig, PortFeatures, PortState)
from tests.test_struct import TestStruct


class TestPortStatus(TestStruct):
    """Test the Port Status message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_port_status')
        super().set_raw_dump_object(_new_portstatus)
        super().set_minimum_size(64)

    def test_pack(self):
        """Skip pack test for now."""
        self.skipTest('Need to recover dump contents.')

    def test_unpack(self):
        """Skipt unpack test for now."""
        self.skipTest('Need to recover dump contents.')


def _new_portstatus():
    """Crate new PortStatus and PhyPort instances."""
    desc_name = 'X' * OFP_MAX_PORT_NAME_LEN
    desc = PhyPort(port_no=2,
                   hw_addr=HWAddress('0a:0a:12:12:10:10'),
                   name=desc_name,
                   config=PortConfig.OFPPC_NO_STP,
                   state=PortState.OFPPS_STP_FORWARD,
                   curr=PortFeatures.OFPPF_10GB_FD,
                   advertised=PortFeatures.OFPPF_PAUSE,
                   supported=PortFeatures.OFPPF_AUTONEG,
                   peer=PortFeatures.OFPPF_AUTONEG)
    return PortStatus(xid=1,
                      reason=PortReason.OFPPR_ADD,
                      desc=desc)
