"""Test for QueueGetConfigReply message."""
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.common.queue import (
    PacketQueue, QueueProperties, QueuePropHeader)
from pyof.v0x01.controller2switch import queue_get_config_reply
from tests.test_struct import TestMsgDumpFile


class TestQueueGetConfigReply(TestMsgDumpFile):
    """Test for QueueGetConfigReply message."""

    dumpfile = 'v0x01/ofpt_queue_get_config_reply.dat'

    properties = [QueuePropHeader(
        queue_property=QueueProperties.OFPQT_MIN_RATE, length=12)]
    queues = [PacketQueue(queue_id=1, length=8,
                          properties=properties)]
    obj = queue_get_config_reply.QueueGetConfigReply(xid=1, port=Port.OFPP_ALL,
                                                     queues=queues)
    min_size = 16
