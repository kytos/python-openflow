"""Testing QueueGetConfigReply message."""
from pyof.v0x04.common.queue import ListOfQueues, PacketQueue
from pyof.v0x04.controller2switch.queue_get_config_reply import (
    QueueGetConfigReply)
from tests.test_struct import TestStruct


class TestQueueGetConfigReply(TestStruct):
    """Test the QueueGetConfigReply message."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'ofpt_queue_get_config_reply')
        super().set_raw_dump_object(QueueGetConfigReply, xid=1, port=1,
                                    queues=_new_list_of_queues())
        super().set_minimum_size(16)


def _new_list_of_queues():
    """Crate new ListOfQueues."""
    queue = PacketQueue(1, 2, 3)
    loq = ListOfQueues([queue, queue])
    return loq
