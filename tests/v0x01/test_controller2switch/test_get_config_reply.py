"""Test GetConfigReply message."""
from pyof.v0x01.controller2switch.common import ConfigFlags
from pyof.v0x01.controller2switch.get_config_reply import GetConfigReply
from tests.test_struct import TestStruct


class TestGetConfigReply(TestStruct):
    """Test class for TestGetConfigReply."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/GetConfigReply] - size 12."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_get_config_reply')
        super().set_raw_dump_object(GetConfigReply, xid=13,
                                    flags=ConfigFlags.OFPC_FRAG_REASM,
                                    miss_send_len=1024)
        super().set_minimum_size(12)
