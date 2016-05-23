import unittest

from pyof.v0x01.asynchronous import packet_in


class TestPacketIn(unittest.TestCase):
    """Test the PacketIn message"""

    def setUp(self):
        """Setup the TestPacketIn Class instantiating a PacketIn message"""
        self.message = packet_in.PacketIn()
        self.message.header.xid = 1
        self.message.buffer_id = 1
        self.message.total_len = 1
        self.message.in_port = 1
        self.message.reason = packet_in.PacketInReason.OFPR_ACTION

    def test_size(self):
        """[Asynchronous/PacketIn] - size 18

        Different from the specification, the minimum size of this class is 18,
        not 20."""
        self.assertEqual(self.message.get_size(), 18)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Asynchronous/PacketIn] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Asynchronous/PacketIn] - unpacking"""
        # TODO
        pass
