"""Echo request message tests."""
from pyof.foundation.basic_types import DPID
from pyof.v0x04.controller2switch.features_reply import FeaturesReply
from tests.unit.test_struct import TestStruct


class TestFeaturesReply(TestStruct):
    """Feature reply message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_features_reply')
        kwargs = _get_kwargs()
        super().set_raw_dump_object(FeaturesReply, **kwargs)
        super().set_minimum_size(32)


def _get_kwargs():
    return {'xid': 3, 'datapath_id': DPID('00:00:00:00:00:00:00:01'),
            'n_buffers': 0, 'n_tables': 254, 'auxiliary_id': 0,
            'capabilities': 0x0000004f, 'reserved': 0x00000000}
