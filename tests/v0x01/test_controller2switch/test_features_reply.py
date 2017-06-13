"""Echo request message tests."""
from pyof.foundation.basic_types import DPID, HWAddress
from pyof.v0x01.common.phy_port import PhyPort, PortConfig, PortState
from pyof.v0x01.controller2switch.features_reply import FeaturesReply
from tests.test_struct import TestStruct


class TestFeaturesReply(TestStruct):
    """Feature reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_features_reply')
        kwargs = _get_kwargs()
        super().set_raw_dump_object(FeaturesReply, **kwargs)
        super().set_minimum_size(32)


def _get_kwargs():
    return {'xid': 2, 'datapath_id': DPID('00:00:00:00:00:00:00:01'),
            'n_buffers': 256, 'n_tables': 254, 'capabilities': 0x000000c7,
            'actions': 4095, 'ports': _get_ports()}


def _get_ports():
    return [
        PhyPort(port_no=65534,
                hw_addr=HWAddress('0e:d3:98:a5:30:47'),
                name='s1',
                config=PortConfig.OFPPC_PORT_DOWN,
                state=PortState.OFPPS_LINK_DOWN,
                curr=0,
                advertised=0,
                supported=0,
                peer=0),
        PhyPort(port_no=1,
                hw_addr=HWAddress('0a:54:cf:fc:4e:6d'),
                name='s1-eth1',
                config=0,
                state=PortState.OFPPS_STP_LISTEN,
                curr=0x000000c0,
                advertised=0,
                supported=0,
                peer=0),
        PhyPort(port_no=2,
                hw_addr=HWAddress('f6:b6:ab:cc:f8:4f'),
                name='s1-eth2',
                config=0,
                state=PortState.OFPPS_STP_LISTEN,
                curr=0x000000c0,
                advertised=0,
                supported=0,
                peer=0)
    ]
