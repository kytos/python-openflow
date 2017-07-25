"""Test for QueueGetConfigRequest message."""
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.controller2switch import queue_get_config_request as request
from tests.test_struct import TestMsgDumpFile


class TestQueueGetConfigRequest(TestMsgDumpFile):
    """Test for QueueGetConfigRequest message."""

    dumpfile = 'v0x01/ofpt_queue_get_config_request.dat'
    obj = request.QueueGetConfigRequest(xid=1, port=Port.OFPP_MAX)
    min_size = 12
