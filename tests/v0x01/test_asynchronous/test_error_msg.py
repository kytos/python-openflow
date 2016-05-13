import unittest

from pyof.v0x01.asynchronous import error_msg


class TestErrorMsg(unittest.TestCase):
    """Test the ErrorMsg message"""

    def setUp(self):
        """Setup the TestErrorMsg Class instantiating a ErrorMsg message"""
        self.message = error_msg.ErrorMsg()
        self.message.header.xid = 1
        self.message.type = error_msg.ErrorType.OFPET_BAD_ACTION
        self.message.code = error_msg.BadActionCode.OFPBAC_EPERM
        self.message.data = []

    def test_size(self):
        """[Asynchronous/ErrorMsg] - size 12"""
        self.assertEqual(self.message.get_size(), 12, 'Wrong message size')

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Asynchronous/ErrorMsg] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Asynchronous/ErrorMsg] - unpacking"""
        # TODO
        pass
