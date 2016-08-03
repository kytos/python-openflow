"""Echo request message tests."""
import unittest
from pyof.v0x01.common.action import ActionType
from pyof.v0x01.controller2switch.features_reply import (Capabilities,
                                                         FeaturesReply)
from tests.teststruct import TestStruct


class TestFeaturesReply(TestStruct):
    """Feature reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_features_reply')
        super().set_raw_dump_object(FeaturesReply, xid=1, datapath_id=1,
                                    n_buffers=1, n_tables=1,
                                    capabilities=Capabilities.OFPC_TABLE_STATS,
                                    actions=ActionType.OFPAT_SET_DL_SRC,
                                    ports=[])
        super().set_minimum_size(32)

    @unittest.skip('Need to recover dump contents.')
    def test_pack(self):
        pass

    @unittest.skip('Need to recover dump contents.')
    def test_unpack(self):
        pass
