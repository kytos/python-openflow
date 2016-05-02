import unittest

from ofp.v0x01.common import queue


class TestQueuePropHeader(unittest.TestCase):

    def setUp(self):
        self.message = queue.QueuePropHeader()
        self.message.property = queue.QueueProperties.OFPQT_MIN_RATE
        self.message.len = 12
        self.message.pad = [0, 0, 0, 0]

    def test_get_size(self):
        """[Common/QueuePropHeader] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/QueuePropHeader] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/QueuePropHeader] - unpacking"""
        # TODO
        pass


class TestPacketQueue(unittest.TestCase):

    def setUp(self):
        propertie01 = queue.QueuePropHeader()
        propertie01.property = queue.QueueProperties.OFPQT_MIN_RATE
        propertie01.len = 12
        propertie01.pad = [0, 0, 0, 0]
        self.message = queue.PacketQueue()
        self.message.queue_id = 1
        self.message.length = 8
        self.message.pad = [0, 0]
        self.message.properties = [propertie01]

    def test_get_size(self):
        """[Common/PacketQueue] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/PacketQueue] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PacketQueue] - unpacking"""
        # TODO
        pass


class TestQueuePropMinRate(unittest.TestCase):

    def setUp(self):
        self.message = queue.QueuePropMinRate()
        self.message.prop_header = queue.QueuePropHeader()
        self.message.prop_header.property = queue.QueueProperties.OFPQT_MIN_RATE
        self.message.prop_header.len = 12
        self.message.prop_header.pad = [0, 0, 0, 0]
        self.message.rate = 1000
        self.message.pad = [0, 0, 0, 0, 0, 0]

    def test_get_size(self):
        """[Common/PropMinRate] - size 16"""
        self.assertEqual(self.message.get_size(), 16)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Common/PropMinRate] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Common/PropMinRate] - unpacking"""
        # TODO
        pass
