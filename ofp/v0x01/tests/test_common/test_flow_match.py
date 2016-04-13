import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')

from common import flow_match
from foundation.base import OFP_ETH_ALEN
from foundation.basic_types import UBInt8Array

class TestOFPMatch(unittest.TestCase):
    def test_get_size(self):
        match = flow_match.OFPMatch(
            1, 22, UBInt8Array(value=123456,length=OFP_ETH_ALEN),
            UBInt8Array(value=123456,length=OFP_ETH_ALEN), 1, 1,
            UBInt8Array(value=0,length=1), 1, 1, 1,
            UBInt8Array(value=0,length=2), 10000, 10000, 22, 22)
        self.assertEqual(match.get_size(), 40)

    def test_pack(self):
        match = flow_match.OFPMatch(
            1, 22, UBInt8Array(value=123456,length=OFP_ETH_ALEN),
            UBInt8Array(value=123456,length=OFP_ETH_ALEN), 1, 1,
            UBInt8Array(value=0,length=1), 1, 1, 1,
            UBInt8Array(value=0,length=2), 10000, 10000, 22, 22)
        match.pack()

    def test_unpack(self):
        pass

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')