"""Testing QueueGetConfigRequest message."""
from pyof.v0x04.controller2switch.queue_get_config_request import (
    QueueGetConfigRequest)
from tests.test_struct import TestStruct


class TestQueueGetConfigRequest(TestStruct):
    """Test the QueueGetConfigRequest message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_queue_get_config_request')
        super().set_raw_dump_object(QueueGetConfigRequest, xid=1, port=1)
        super().set_minimum_size(16)
