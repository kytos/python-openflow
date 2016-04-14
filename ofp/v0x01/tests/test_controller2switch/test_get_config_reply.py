import unittest

from ofp.v0x01.controller2switch import get_config_reply


class TestSwitchConfig(unittest.TestCase):

    def test_get_size(self):
        get_config_reply_message = \
            get_config_reply.SwitchConfig(xid=1, set_message=False, flags=1,
                                          miss_send_len=1024*1024)
        self.assertEqual(get_config_reply_message.get_size(), 16)

    def test_pack(self):
        get_config_reply_message = \
            get_config_reply.SwitchConfig(xid=1, set_message=False, flags=1,
                                          miss_send_len=1024*1024)
        get_config_reply_message.pack()

    def test_unpack(self):
        pass
