"""Port Status message tests."""
from pyof.foundation.basic_types import HWAddress
from pyof.foundation.constants import OFP_MAX_PORT_NAME_LEN
from pyof.v0x01.asynchronous.port_status import PortReason, PortStatus
from pyof.v0x01.common.phy_port import (
    PhyPort, PortConfig, PortFeatures, PortState)
from tests.test_struct import TestMsgDump, TestMsgDumpFile


class TestPortStatus_1(TestMsgDumpFile):
    """Test the PortStatus class."""

    dumpfile = 'v0x01/ofpt_port_status.dat'

    desc_name = 's1-eth1'
    desc = PhyPort(port_no=1,
                   hw_addr=HWAddress('9a:da:11:8a:f4:0c'),
                   name=desc_name,
                   config=0,
                   state=0,
                   curr=192,
                   advertised=0,
                   supported=0,
                   peer=0)
    obj = PortStatus(xid=0,
                     reason=PortReason.OFPPR_MODIFY,
                     desc=desc)


class TestPortStatus_2(TestMsgDump):
    """Test the PortStatus class."""

    dump = b'\x01\x0c\x00@\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
    dump += b'\x00\x00\x02\n\n\x12\x12\x10\x10XXXXXXXXXXXXXXX\x00\x00\x00'
    dump += b'\x00\x02\x00\x00\x02\x00\x00\x00\x00@\x00\x00\x04\x00\x00'
    dump += b'\x00\x02\x00\x00\x00\x02\x00'  # needs to be checked

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
    obj = PortStatus(xid=1,
                     reason=PortReason.OFPPR_ADD,
                     desc=desc)
