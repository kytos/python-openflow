import unittest

from ofp.v0x01.common import port
from ofp.v0x01.controller2switch import features_reply
from ofp.v0x01.foundation import base

class TestSwitchFeatures(unittest.TestCase):

    def test_get_size(self):
        hw_addr = [100, 50, 48, 48, 160, 160]
        name = bytes("".join(['X' for _ in range(base.OFP_MAX_PORT_NAME_LEN)]),
                     'utf-8')
        of_port = port.Port(port_no=80, hw_addr=hw_addr, name=name, config=1<<1,
                     state=3<<8, curr=0, advertised=1<<4, supported=1<<4,
                     peer=1<<4)
        switch_features = \
            features_reply.SwitchFeatures(xid=1, datapath_id=1, n_buffers=1,
                                          n_tables=1, pad=[0, 0, 0],
                                          capabilities=1, actions=5,
                                          ports=of_port)
        self.assertEqual(switch_features.get_size(), 80)

    def test_pack(self):
        hw_addr = [100, 50, 48, 48, 160, 160]
        name = bytes("".join(['X' for _ in range(base.OFP_MAX_PORT_NAME_LEN)]),
                     'utf-8')
        of_port = port.Port(port_no=80, hw_addr=hw_addr, name=name, config=1<<1,
                     state=3<<8, curr=0, advertised=1<<4, supported=1<<4,
                     peer=1<<4)
        switch_features = \
            features_reply.SwitchFeatures(xid=1, datapath_id=1, n_buffers=1,
                                          n_tables=1, pad=[0, 0, 0],
                                          capabilities=1, actions=5,
                                          ports=of_port)
        switch_features.pack()

    def test_unpack(self):
        pass
