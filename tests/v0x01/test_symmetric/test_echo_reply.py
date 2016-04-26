import unittest

from ofp.v0x01.symmetric import echo_reply


class TestOFPReply(unittest.TestCase):

    def setUp(self):
        self.message = echo_reply.OFPReply(xid=3)

    def test_get_size(self):
        """[Symmetric/OFPReply] - size 8"""
        self.assertEqual(self.message.get_size(), 8)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Symmetric/OFPReply] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Symmetric/OFPReply] - unpacking"""
        # TODO
        pass
