"""Testing Header structure."""
import unittest

from pyof.foundation.exceptions import PackException
from pyof.v0x01.common.header import Header, Type
from tests.test_struct import TestStructDump


class TestHeader(TestStructDump):
    """Test the message Header."""

    dump = b'\x01\x00\x00\x08\x00\x00\x00\x01'
    obj = Header(message_type=Type.OFPT_HELLO,
                 xid=1,
                 length=8)

    @unittest.expectedFailure
    def test_pack_empty(self):
        """[Common/Header] - packing empty header."""
        self.assertRaises(PackException,
                          Header().pack())

    # @patch('pyof.v0x01.common.header.randint')
    # def test_random_xid(self, m):
    #     """Each Header instantiations without xid should call randint."""
    #     Header(), Header()  # noqa
    #     self.assertEqual(m.call_count, 2)
