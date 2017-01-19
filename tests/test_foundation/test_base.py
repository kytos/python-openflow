"""Test Base module of python-openflow."""
import unittest

from pyof.foundation import base, basic_types


class TestGenericStruct(unittest.TestCase):
    """Testing GenericStruct class."""

    def setUp(self):
        """Basic Test Setup."""
        class AttributeA(base.GenericStruct):
            """Example class."""

            a1 = basic_types.UBInt8(1)
            a2 = basic_types.UBInt16(2)

        class AttributeC(base.GenericStruct):
            """Example class."""

            c1 = basic_types.UBInt32(3)
            c2 = basic_types.UBInt64(4)

        class AttributeB(base.GenericStruct):
            """Example class."""

            c = AttributeC()

        class Header(base.GenericStruct):
            """Mock Header class."""

            version = basic_types.UBInt8(1)
            message_type = basic_types.UBInt8(2)
            length = basic_types.UBInt8(8)
            xid = basic_types.UBInt8(4)

        class MyMessage(base.GenericMessage):
            """Example class."""

            header = Header()
            a = AttributeA()
            b = AttributeB()
            i = basic_types.UBInt32(5)

            def __init__(self):
                """Init method of example class."""
                super().__init__(None)

        self.MyMessage = MyMessage

    def test_basic_attributes(self):
        """[Foundation/Base/GenericStruct] - Attributes Creation."""
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


class TestGenericType(unittest.TestCase):
    """Testing GenericType class."""

    def test_basic_operator(self):
        """[Foundation/Base/GenericType] - Basic Operators."""
        a = basic_types.UBInt32(1)
        b = basic_types.UBInt32(2)

        self.assertEqual(a + 1, 2)
        self.assertEqual(1 + a, 2)
        self.assertEqual(b + 1, 3)
        self.assertEqual(1 + b, 3)

        self.assertEqual(a - 1, 0)
        self.assertEqual(1 - a, 0)
        self.assertEqual(b - 1, 1)
        self.assertEqual(1 - b, 1)

        self.assertEqual(a & 1, 1)
        self.assertEqual(1 & a, 1)
        self.assertEqual(b & 1, 0)
        self.assertEqual(1 & b, 0)

        self.assertEqual(a | 1, 1)
        self.assertEqual(1 | a, 1)
        self.assertEqual(b | 1, 3)
        self.assertEqual(1 | b, 3)

        self.assertEqual(a ^ 1, 0)
        self.assertEqual(1 ^ a, 0)
        self.assertEqual(b ^ 1, 3)
        self.assertEqual(1 ^ b, 3)
