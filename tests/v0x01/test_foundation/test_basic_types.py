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


class TestUBInt8Array(unittest.TestCase):

    def setUp(self):
        self.item = basic_types.UBInt8Array(value=[15, 15, 15, 15, 15, 15],
                                            length=6)

    def test_size(self):
        """[Foundation/BasicTypes/UBInt8Array] - size 6"""
        self.assertEqual(self.item.get_size(), 6)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Foundation/BasicTypes/UBInt8Array] - packing"""
        # TODO
        pass

    @unittest.skip('Not yet implemented')
    def test_unpack(self):
        """[Foundation/BasicTypes/UBInt8Array] - unpacking"""
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
