"""Set Config message tests."""
from pyof.v0x01.controller2switch.common import ConfigFlag
from pyof.v0x01.controller2switch.set_config import SetConfig
from tests.test_struct import TestStruct


class TestSetConfig(TestStruct):
    """Test the Set Config message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_set_config')
        super().set_raw_dump_object(SetConfig, xid=3,
                                    flags=ConfigFlag.OFPC_FRAG_NORMAL,
                                    miss_send_len=128)
        super().set_minimum_size(12)
