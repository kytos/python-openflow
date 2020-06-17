"""Set Config message tests."""
from pyof.v0x04.common.action import ControllerMaxLen
from pyof.v0x04.controller2switch.common import ConfigFlag
from pyof.v0x04.controller2switch.set_config import SetConfig
from tests.unit.test_struct import TestStruct


class TestSetConfig(TestStruct):
    """Test the Set Config message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        buffer = ControllerMaxLen.OFPCML_NO_BUFFER
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_set_config')
        super().set_raw_dump_object(SetConfig, xid=1201346349,
                                    flags=ConfigFlag.OFPC_FRAG_NORMAL,
                                    miss_send_len=buffer)
        super().set_minimum_size(12)
