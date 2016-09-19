"""Port Status message tests."""
from pyof.foundation.basic_types import HWAddress
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x04.asynchronous.port_status import PortReason, PortStatus
from pyof.v0x04.common.port import Port, PortConfig, PortFeatures, PortState
from tests.test_struct import TestStruct


class TestPortStatus(TestStruct):
    """Test the Port Status message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_port_status')
        super().set_raw_dump_object(_new_portstatus)
        super().set_minimum_size(80)


def _new_portstatus():
    """Crate new PortStatus and Port instances."""
    desc_name = 'X' * OFP_MAX_PORT_NAME_LEN
    desc = Port(port_no=2,
                hw_addr=HWAddress('0a:0a:12:12:10:10'),
                name=desc_name,
                config=PortConfig.OFPPC_PORT_DOWN,
                state=PortState.OFPPS_LINK_DOWN,
                curr=PortFeatures.OFPPF_10GB_FD,
                advertised=PortFeatures.OFPPF_PAUSE,
                supported=PortFeatures.OFPPF_AUTONEG,
                peer=PortFeatures.OFPPF_AUTONEG)
    return PortStatus(xid=1,
                      reason=PortReason.OFPPR_ADD,
                      desc=desc)
