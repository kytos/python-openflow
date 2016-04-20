import unittest

from ofp.v0x01.symmetric import echo_request

class TestOFPRequest(unittest.TestCase):
    def test_get_size(self):
        request_message = echo_request.OFPRequest(xid=2)
        self.assertEqual(request_message.get_size(), 8)

    def test_pack(self):
        request_message = echo_request.OFPRequest(xid=2)
        request_message.pack()

    def test_unpack(self):
        pass
