"""Test for QueueGetConfigRequest message."""
import unittest

from pyof.v0x01.controller2switch import queue_get_config_request


class TestQueueGetConfigRequest(unittest.TestCase):
    """Test for QueueGetConfigRequest message."""

    def setUp(self):
        """Baisc test setup."""
        self.message = queue_get_config_request.QueueGetConfigRequest()
        self.message.header.xid = 1
        self.message.port = 80

    def test_get_size(self):
        """[Controller2Switch/QueueGetConfigRequest] - size 12."""
        self.assertEqual(self.message.get_size(), 12)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/QueueGetConfigRequest] - packing."""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Controller2Switch/QueueGetConfigRequest] - unpacking."""
        # TODO
        pass
