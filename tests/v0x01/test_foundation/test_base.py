import unittest

from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types


class TestGenericStruct(unittest.TestCase):

    def setUp(self):
        class AttributeA(base.GenericStruct):
            a1 = basic_types.UBInt8(1)
            a2 = basic_types.UBInt16(2)

        class AttributeC(base.GenericStruct):
            c1 = basic_types.UBInt32(3)
            c2 = basic_types.UBInt64(4)

        class AttributeB(base.GenericStruct):
            c = AttributeC()

        class MyMessage(base.GenericMessage):
            a = AttributeA()
            b = AttributeB()
            i = basic_types.UBInt32(5)

            def __init__(self):
                base.GenericStruct.__init__(self)

        self.MyMessage = MyMessage

    def test_basic_attributes(self):
        """[Foundation/Base/GenericStruct] - Attributes Creation"""
        message1 = self.MyMessage()
        message2 = self.MyMessage()
        self.assertIsNot(message1, message2)
        self.assertIsNot(message1.i, message2.i)
        self.assertIsNot(message1.a, message2.a)
        self.assertIsNot(message1.b, message2.b)
        self.assertIsNot(message1.a.a1, message2.a.a1)
        self.assertIsNot(message1.a.a2, message2.a.a2)
        self.assertIsNot(message1.b.c, message2.b.c)
        self.assertIsNot(message1.b.c.c1, message2.b.c.c1)
        self.assertIsNot(message1.b.c.c2, message2.b.c.c2)
