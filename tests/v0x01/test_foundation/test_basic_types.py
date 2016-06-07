import unittest

from pyof.v0x01.foundation import basic_types


class TestUBInt8(unittest.TestCase):

    def setUp(self):
        self.ubint8 = basic_types.UBInt8()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt8] - size 1"""
        self.assertEqual(self.ubint8.get_size(), 1)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt8] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt8] - unpacking"""
        # TODO
        pass


class TestUBInt16(unittest.TestCase):

    def setUp(self):
        self.ubint16 = basic_types.UBInt16()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt16] - size 2"""
        self.assertEqual(self.ubint16.get_size(), 2)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt16] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt16] - unpacking"""
        # TODO
        pass


class TestUBInt32(unittest.TestCase):

    def setUp(self):
        self.ubint32 = basic_types.UBInt32()

    def test_get_size(self):
        """[Foundation/BasicTypes/UBInt32] - size 4"""
        self.assertEqual(self.ubint32.get_size(), 4)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt32] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt32] - unpacking"""
        # TODO
        pass

class TestChar(unittest.TestCase):

    def setUp(self):
        self.char1 = basic_types.Char('foo', length=3)
        self.char2 = basic_types.Char('foo', length=5)

    def test_get_size(self):
        """[Foundation/BasicTypes/Char] - get_size"""
        self.assertEqual(self.char1.get_size(), 3)
        self.assertEqual(self.char2.get_size(), 5)

    def test_pack(self):
        """[Foundation/BasicTypes/Char] - packing"""
        self.assertEqual(self.char1.pack(), b'fo\x00')
        self.assertEqual(self.char2.pack(), b'foo\x00\x00')

    def test_unpack(self):
        """[Foundation/BasicTypes/Char] - unpacking"""
        char1 = basic_types.Char(length=3)
        char2 = basic_types.Char(length=5)
        char1.unpack(b'fo\x00')
        char2.unpack(b'foo\x00\x00')

        self.assertEqual(char1.value, 'fo')
        self.assertEqual(char2.value, 'foo')
