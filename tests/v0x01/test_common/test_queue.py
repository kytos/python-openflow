"""Testing Queue structure."""
from pyof.v0x01.common import queue
from tests.test_struct import TestStructDump


class TestQueuePropHeader(TestStructDump):
    """Test QueuePropHeader."""

    dump = b'\x00\x01\x00\x0c\x00\x00\x00\x00'  # needs to be checked
    obj = queue.QueuePropHeader(
        queue_property=queue.QueueProperties.OFPQT_MIN_RATE,
        length=12)


class TestPacketQueue(TestStructDump):
    """TestPacketQueue."""

    dump = b'\x00\x00\x00\x01\x00\x08\x00\x00'  # needs to be checked
    obj = queue.PacketQueue(queue_id=1,
                            length=8)


class TestQueuePropMinRate(TestStructDump):
    """Test QueuePropMinRate."""

    dump = b'\x00\x01\x00\x10\x00\x00\x00\x00\x03\xe8\x00\x00'
    dump += b'\x00\x00\x00\x00'  # needs to be checked
    obj = queue.QueuePropMinRate(rate=1000)
