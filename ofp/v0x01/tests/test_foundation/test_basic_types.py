import unittest
import sys
import os

from ofp.v0x01.foundation import basic_types


class TestUBInt8(unittest.TestCase):

    def test_get_size(self):
        ubint8 = basic_types.UBInt8()
        self.assertEqual(ubint8.get_size(), 1)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass


class TestUBInt8Array(unittest.TestCase):

    def test_get_size(self):
        ubint8_array = basic_types.UBInt8Array(value=255, length=6)
        ubint8_array._value = [15, 15, 15, 15, 15, 15]
        self.assertEqual(ubint8_array.get_size(), 6)

    def test_pack(self):
        ubint8_array = basic_types.UBInt8Array(value=255, length=6)
        ubint8_array._value = [15, 15, 15, 15, 15, 15]
        ubint8_array.pack()

    def test_unpack(self):
        pass


class TestUBInt16(unittest.TestCase):

    def test_get_size(self):
        ubint16 = basic_types.UBInt16()
        self.assertEqual(ubint16.get_size(), 2)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass


class TestUBInt32(unittest.TestCase):

    def test_get_size(self):
        ubint32 = basic_types.UBInt32()
        self.assertEqual(ubint32.get_size(), 4)

    def test_pack(self):
        pass

    def test_unpack(self):
        pass
