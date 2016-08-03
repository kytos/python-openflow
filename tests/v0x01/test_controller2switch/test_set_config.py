"""Set Config message tests."""
import unittest

from pyof.v0x01.controller2switch.flow_mod import FlowModFlags
from pyof.v0x01.controller2switch.set_config import SetConfig
from tests.teststruct import TestStruct


class TestSetConfig(TestStruct):
    """Test the Set Config message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_set_config')
        super().set_raw_dump_object(SetConfig, xid=1,
                                    flags=FlowModFlags.OFPFF_EMERG,
                                    miss_send_len=1024)
        super().set_minimum_size(12)

    @unittest.skip('Need to recover dump contents.')
    def test_pack(self):
        pass

    @unittest.skip('Need to recover dump contents.')
    def test_unpack(self):
        pass
