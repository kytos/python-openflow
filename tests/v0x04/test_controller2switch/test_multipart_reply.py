"""MultipartReply message test."""

from pyof.v0x04.controller2switch.common import (MeterConfig, MultipartTypes)
from pyof.v0x04.controller2switch.meter_mod import (MeterFlags, Meter,
                                                    MeterBandDrop,
                                                    MeterBandDscpRemark,
                                                    ListOfMeterBandHeader)
from pyof.v0x04.controller2switch.multipart_reply import (MultipartReply,
                                                          MultipartReplyFlags)
from tests.v0x04.test_struct import TestStruct

class TestTableFeatures(TestStruct):
    """"""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=16,
                            multipart_type=MultipartTypes.OFPMP_METER_CONFIG,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body=cls.meter_config_instance())
        super().set_minimum_size(16)

    @classmethod
    def meter_config_instance(cls):
        """Method used to create a MeterConfig instance."""
        return MeterConfig(bands=cls.list_of_meters())

    @staticmethod
    def list_of_meters():
        """Method used to instantiate a ListOfMeterBandHeader with some instances."""
        meters = [MeterBandDrop(rate=6, burst_size=3),
                  MeterBandDscpRemark(rate=1,burst_size=4,prec_level=2),
                  MeterBandDrop(rate=9, burst_size=1)]
        return ListOfMeterBandHeader(items=[meters])
