"""Set Config message tests."""
from pyof.v0x01.controller2switch.common import ConfigFlags
from pyof.v0x01.controller2switch.set_config import SetConfig
from tests.test_struct import TestMsgDumpFile


class TestSetConfig(TestMsgDumpFile):
    """Test the Set Config message."""

    dumpfile = 'v0x01/ofpt_set_config.dat'
    obj = SetConfig(xid=3, flags=ConfigFlags.OFPC_FRAG_NORMAL,
                    miss_send_len=128)
    min_size = 12
