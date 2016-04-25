import unittest

from ofp.v0x01.asynchronous import port_status
from ofp.v0x01.common import phy_port
from ofp.v0x01.foundation import base


class TestPortStatus(unittest.TestCase):
    """Test the PortStatus message"""

    def setUp(self):
        """Setup the TestPortStatus Class"""
        hw_addr = [100, 50, 48, 48, 160, 160]
        name = bytes("".join(['X' for _ in range(base.OFP_MAX_PORT_NAME_LEN)]),
                     'utf-8')
        port = phy_port.PhyPort(port_no=80, hw_addr=hw_addr, name=name,
                                config=1 << 1, state=3 << 8, curr=0,
                                advertised=1 << 4, supported=1 << 4,
                                peer=1 << 4)
        self.message = port_status.PortStatus(xid=1,
                                              reason=port_status.PortReason.OFPPR_ADD,
                                              pad=[1, 1, 1, 1, 1, 1, 1],
                                              desc=port)

    def test_size(self):
        """Test the size of the message"""
        self.assertEqual(self.header.get_size(), 64)

    def test_pack(self):
        """Test the pack method for the PortStatus"""
        packet_message = b'\x01\x00\x00\x00\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packet_message)

    def test_unpack(self):
        """Test message unpacking.
        Should read a raw binary datapack, get the first 8 bytes and
        then unpack it as a PortStatus object."""
        # TODO
        # self.assertEqual(unpacked_header, self.header)
        pass
