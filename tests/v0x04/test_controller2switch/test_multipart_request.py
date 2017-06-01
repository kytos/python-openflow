"""MultipartRequest message test."""
from pyof.v0x04.controller2switch.multipart_request import (
    MultipartRequest, MultipartRequestFlags, MultipartTypes, PortStatsRequest,
    TableFeatures)
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

    @staticmethod
    def get_attributes(multipart_type=MultipartTypes.OFPMP_DESC,
                       flags=MultipartRequestFlags.OFPMPF_REQ_MORE,
                       body=''):
        """Method used to return a dict with instance paramenters."""
        return {'xid': 32, 'multipart_type': multipart_type, 'flags': flags,
                'body': body}

    def test_pack_unpack_desc(self):
        """Testing multipart_type with OFPMP_DESC."""
        options = TestMultipartRequest.get_attributes(
            multipart_type=MultipartTypes.OFPMP_DESC)
        self._test_pack_unpack(**options)

    def test_pack_unpack_table(self):
        """Testing multipart_type with OFPMP_TABLE."""
        options = TestMultipartRequest.get_attributes(
            multipart_type=MultipartTypes.OFPMP_TABLE)
        self._test_pack_unpack(**options)

    def test_pack_unpack__port_stats_request(self):
        """Testing multipart_type with OFPMP_PORT_STATS."""
        options = TestMultipartRequest.get_attributes(
            multipart_type=MultipartTypes.OFPMP_PORT_STATS,
            body=PortStatsRequest(port_no=33))
        self._test_pack_unpack(**options)

    def test_pack_unpack_port_desc(self):
        """Testing multipart_type with OFPMP_PORT_DESC."""
        options = TestMultipartRequest.get_attributes(
            multipart_type=MultipartTypes.OFPMP_PORT_DESC)
        self._test_pack_unpack(**options)

    def test_pack_unpack_table_features(self):
        """Testing multipart_type with OFPMP_TABLE_FEATURES."""
        instance = [TableFeatures(table_id=2),
                    TableFeatures(table_id=6),
                    TableFeatures(table_id=4)]
        options = TestMultipartRequest.get_attributes(
            multipart_type=MultipartTypes.OFPMP_TABLE_FEATURES,
            body=instance)
        self._test_pack_unpack(**options)
