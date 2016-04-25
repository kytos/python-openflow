import unittest

from ofp.v0x01.asynchronous import error_msg


class TestErrorMsg(unittest.TestCase):
    """Test the ErrorMsg message"""

    def setUp(self):
        """Setup the TestErrorMsg Class instantiating a ErrorMsg message"""
        self.message = error_msg.ErrorMsg(xid=1,
                                          type=error_msg.ErrorType.OFPET_BAD_ACTION,
                                          code=error_msg.BadActionCode.OFPBAC_EPERM,
                                          data=[0])

    def test_size(self):
        """Test the size of the message"""
        self.assertEqual(self.message.get_size(), 12)

    def test_pack(self):
        """Test the pack method for the packetIn"""
        packet_message = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packet_message)

    def test_unpack(self):
        """Test unpacking.
        Should read a raw binary datapack, get the first 8 bytes and
        then unpack it as a ErrorMsg object."""
        # TODO
        # self.assertEqual(unpacked_header, self.header)
        pass
