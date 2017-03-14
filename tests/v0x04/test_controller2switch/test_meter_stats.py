"""Test of v0x04 meter stats module."""


from pyof.v0x04.controller2switch.common import BandStats, MeterStats
from pyof.v0x04.controller2switch.multipart_reply import (MultipartReply,
                                                          MultipartTypes,
                                                          MultipartReplyFlags)
from tests.v0x04.test_struct import TestStruct

class TestMeterStats(TestStruct):
    """"""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=16,
                            multipart_type=MultipartTypes.OFPMP_METER,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body=cls.get_meter_stats_instance())
        super().set_minimum_size(16)

    @classmethod
    def get_meter_stats_instance(cls):
        """Method used to create a MeterStats instance."""
        return MeterStats(flow_count=2,packet_in_count=23, byte_in_count=44,
                          duration_sec=33, duration_nsec=99,
                          band_stats=cls.get_list_of_bands_stats())

    @staticmethod
    def get_list_of_bands_stats():
       """Method used to return a list of BandStats."""
       return [BandStats(byte_band_count=200,packet_band_count=300),
               BandStats(byte_band_count=400,packet_band_count=500),
               BandStats(byte_band_count=600,packet_band_count=700)]

