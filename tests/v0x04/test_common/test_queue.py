"""Test of v0x04 queue module."""
from pyof.v0x04.common.queue import (
    PacketQueue, QueuePropExperimenter, QueuePropHeader, QueuePropMaxRate,
    QueuePropMinRate)
from tests.test_struct import TestStruct


class TestPacketQueue(TestStruct):
    """Packet Queue structure tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'packet_queue')
        super().set_raw_dump_object(PacketQueue)
        super().set_minimum_size(16)


class TestQueuePropExperimenter(TestStruct):
    """QueuePropExperimenter tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'queue_prop_experimenter')
        super().set_raw_dump_object(QueuePropExperimenter)
        super().set_minimum_size(16)


class TestQueuePropHeader(TestStruct):
    """QueuePropHeader structure tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'queue_prop_header')
        super().set_raw_dump_object(QueuePropHeader)
        super().set_minimum_size(8)


class TestQueuePropMaxRate(TestStruct):
    """QueuePropMaxRate structure tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'queue_prop_max_rate')
        super().set_raw_dump_object(QueuePropMaxRate)
        super().set_minimum_size(16)


class TestQueuePropMinRate(TestStruct):
    """QueuePropMinRate structure tests (also those in :class:`.TestDump`)."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_raw_dump_file('v0x04', 'queue_prop_min_rate')
        super().set_raw_dump_object(QueuePropMinRate)
        super().set_minimum_size(16)
