import unittest

from ofp.v0x01.asynchronous import packet_in


class TestPacketIn(unittest.TestCase):
    """Test the PacketIn message"""

    def setUp(self):
        """Setup the TestPacketIn Class instantiating a PacketIn message"""
        self.message = packet_in.PacketIn(xid=1, buffer_id=1, total_len=1,
                                          in_port=1,
                                          reason=packet_in.PacketInReason.OFPR_ACTION,
                                          pad=1, data=[0])

    def test_size(self):
        """Test the size of the message"""
        self.assertEqual(self.header.get_size(), 20)

    def test_pack(self):
        """Test the pack method for the packetIn"""
        packet_message = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packet_message)

    def test_unpack(self):
        """Test unpacking.
        Should read a raw binary datapack, get the first 8 bytes and
        then unpack it as a PacketIn object."""
        # TODO
        # self.assertEqual(unpacked_header, self.header)
        pass
