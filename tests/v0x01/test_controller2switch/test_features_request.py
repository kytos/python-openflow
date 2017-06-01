"""Feature request message tests."""
from pyof.v0x01.controller2switch.features_request import FeaturesRequest
from tests.test_struct import TestStruct


class TestFeaturesRequest(TestStruct):
    """Feature request message tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_features_request')
        super().set_raw_dump_object(FeaturesRequest, xid=3)
        super().set_minimum_size(8)
