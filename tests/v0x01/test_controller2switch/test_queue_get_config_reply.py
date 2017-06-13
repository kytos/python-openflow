"""Test for QueueGetConfigReply message."""
from pyof.v0x01.common.phy_port import Port
from pyof.v0x01.common.queue import (
    PacketQueue, QueueProperties, QueuePropHeader)
from pyof.v0x01.controller2switch import queue_get_config_reply
from tests.test_struct import TestStruct


class TestQueueGetConfigReply(TestStruct):
    """Test for QueueGetConfigReply message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/QueueGetConfigReply] - size 16."""
        super().setUpClass()
        super().set_raw_dump_file('v0x01', 'ofpt_queue_get_config_reply')
        super().set_raw_dump_object(queue_get_config_reply.QueueGetConfigReply,
                                    xid=1, port=Port.OFPP_ALL,
                                    queues=_get_packet_queue())
        super().set_minimum_size(16)


def _get_packet_queue():
    """Function used to return a PacketQueue instance."""
    packets = []
    packets.append(PacketQueue(queue_id=1, length=8,
                               properties=_get_queue_properties()))
    return packets


def _get_queue_properties():
    """Function used to return a list of queue properties."""
    properties = []
    properties.append(QueuePropHeader(
        queue_property=QueueProperties.OFPQT_MIN_RATE, length=12))
    return properties
