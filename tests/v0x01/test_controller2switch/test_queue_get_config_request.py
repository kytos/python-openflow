"""Test for QueueGetConfigRequest message."""
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch import queue_get_config_request as request
from tests.test_struct import TestStruct


class TestQueueGetConfigRequest(TestStruct):
    """Test for QueueGetConfigRequest message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/QueueGetConfigRequest] - size 12."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_queue_get_config_request')
        super().set_raw_dump_object(request.QueueGetConfigRequest,
                                    xid=1, port=Port.OFPP_MAX)
        super().set_minimum_size(12)
