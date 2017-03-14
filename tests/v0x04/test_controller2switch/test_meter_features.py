"""Test of v0x04 meter features module."""

from pyof.v0x04.controller2switch.common import MeterFeatures, MultipartTypes
from pyof.v0x04.controller2switch.meter_mod import MeterBandType, MeterFlags
from pyof.v0x04.controller2switch.multipart_reply import (MultipartReply,
                                                          MultipartReplyFlags)

from tests.v0x04.test_struct import TestStruct

class TestMeterFeatures(TestStruct):
    """Class to test MeterFeatures structures."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=17,
                            multipart_type=MultipartTypes.OFPMP_METER_FEATURES,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body=cls.meter_feature_instance())
        super().set_minimum_size(16)

    @classmethod
    def meter_feature_instance(cls):
        """Method used to create a MeterFeature instance."""
        return MeterFeatures(max_meter=200,max_bands=20, max_color=4,
                             band_types=MeterBandType.OFPMBT_DROP,
                             capabilities=MeterFlags.OFPMF_KBPS)
