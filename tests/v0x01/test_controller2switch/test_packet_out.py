import unittest

from ofp.v0x01.controller2switch import packet_out


class TestPacketOut(unittest.TestCase):
    def setUp(self):
        self.message = packet_out.PacketOut(xid=80, buffer_id=5, in_pot=80,
                                            actions_len=4, data=[0])

    def test_get_size(self):
        self.assertEqual(self.message.get_size(), 16)

    def test_pack(self):
        self.message.pack()

    def test_unpack(self):
        pass
