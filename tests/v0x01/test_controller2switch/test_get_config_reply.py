"""Test GetConfigReply message."""
from pyof.v0x01.controller2switch.common import ConfigFlags
from pyof.v0x01.controller2switch.get_config_reply import GetConfigReply
from tests.test_struct import TestMsgDumpFile


class TestGetConfigReply(TestMsgDumpFile):
    """Test class for TestGetConfigReply."""

    dumpfile = 'v0x01/ofpt_get_config_reply.dat'
    obj = GetConfigReply(xid=13,
                         flags=ConfigFlags.OFPC_FRAG_REASM,
                         miss_send_len=1024)
    min_size = 12
