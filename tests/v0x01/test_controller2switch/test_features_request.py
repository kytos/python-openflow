"""Feature request message tests."""
from pyof.v0x01.controller2switch.features_request import FeaturesRequest
from tests.test_struct import TestMsgDumpFile


class TestFeaturesRequest(TestMsgDumpFile):
    """Feature request message tests (also those in :class:`.TestDump`)."""

    dumpfile = 'v0x01/ofpt_features_request.dat'
    obj = FeaturesRequest(xid=3)
    min_size = 8
