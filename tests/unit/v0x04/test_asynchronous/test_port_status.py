"""Port Status message tests."""
from pyof.foundation.basic_types import HWAddress
from pyof.v0x04.asynchronous.port_status import PortReason, PortStatus
from pyof.v0x04.common.port import Port, PortFeatures, PortState
from tests.unit.test_struct import TestStruct


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
    desc_name = 's1-eth1'
    desc = Port(port_no=1,
                hw_addr=HWAddress('62:43:e5:db:35:0a'),
                name=desc_name,
                config=0,
                state=PortState.OFPPS_LIVE,
                curr=PortFeatures.OFPPF_10GB_FD | PortFeatures.OFPPF_COPPER,
                advertised=0,
                supported=0,
                peer=0,
                curr_speed=10000000,
                max_speed=0)
    return PortStatus(xid=0,
                      reason=PortReason.OFPPR_MODIFY,
                      desc=desc)
