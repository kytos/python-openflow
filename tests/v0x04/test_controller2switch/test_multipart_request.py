"""MultipartRequest message test."""
from pyof.v0x04.controller2switch.multipart_request import (
    MultipartRequest, MultipartRequestFlags, MultipartTypes, TableFeatures)

from tests.v0x04.test_struct import TestStruct


class TestMultipartRequest(TestStruct):
    """Test the MultipartRequest message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()

        super().set_message(MultipartRequest, xid=16,
                            multipart_type=MultipartTypes.OFPMP_TABLE_FEATURES,
                            flags=MultipartRequestFlags.OFPMPF_REQ_MORE,
                            body=b'')
        super().set_minimum_size(16)

    def test_body_table_features(self):
        """Method to test pack and unpack using table_features as body."""
        table_features = [TableFeatures(table_id=2),
                          TableFeatures(table_id=6),
                          TableFeatures(table_id=4)]

        options = {'xid': 16,
                   'multipart_type': MultipartTypes.OFPMP_TABLE_FEATURES,
                   'flags': MultipartRequestFlags.OFPMPF_REQ_MORE,
                   'body': table_features}
        self._test_pack_unpack(**options)
