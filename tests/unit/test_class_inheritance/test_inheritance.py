"""Testing class inheritance attributes changes."""
import unittest

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import UBInt8, UBInt16, UBInt32, UBInt64


class TestInheritance(unittest.TestCase):
    """Testing GenericStruct class inheritance."""

    def setUp(self):
        """Basic Test Setup."""
        class MyClassA(GenericStruct):
            """Example class."""

            a1 = UBInt8(1)
            a2 = UBInt16(2)
            a3 = UBInt8(3)
            a4 = UBInt16(4)
            a5 = UBInt32(5)

        class MyClassB(MyClassA):
            """Example class."""

            a0 = UBInt32(0)
            a2 = UBInt64(2)
            b6 = UBInt8(6)

            _removed_attributes = ['a3']
            # _rename_attributes = [('a4', 'b4')]
            # _insert_attributes_before = {'a0': 'a1'}

        self.MyClassA = MyClassA
        self.MyClassB = MyClassB
        self.a_expected_names = ['a1', 'a2', 'a3', 'a4', 'a5']
        self.b_expected_names = ['a1', 'a2', 'a4', 'a5', 'a0', 'b6']
        # self.b_expected_names = ['a0', 'a1', 'a2', 'b4', 'a5', 'b6']

    def test_modifications(self):
        """[Foundation/Base/GenericStruct] - Attributes Modifications."""
        m1 = self.MyClassA()
        m2 = self.MyClassB()
        # Checking keys (attributes names) and its ordering
        self.assertEqual([attr[0] for attr in m1.get_class_attributes()],
                         self.a_expected_names)
        self.assertEqual([attr[0] for attr in m2.get_class_attributes()],
                         self.b_expected_names)

        # Check if there is no shared attribute between instances
        self.assertIsNot(m1, m2)
        self.assertIsNot(m1.a1, m2.a1)
        self.assertIsNot(m1.a2, m2.a2)
        self.assertIsNot(m1.a3, m2.a4)
        self.assertIsNot(m1.a4, m2.a4)
        self.assertIsNot(m1.a5, m2.a5)

        # Check attributes types on MyClassA
        self.assertIsInstance(self.MyClassA.a1, UBInt8)
        self.assertIsInstance(self.MyClassA.a2, UBInt16)
        self.assertIsInstance(self.MyClassA.a3, UBInt8)
        self.assertIsInstance(self.MyClassA.a4, UBInt16)
        self.assertIsInstance(self.MyClassA.a5, UBInt32)

        # Check attributes types on MyClassA
        self.assertIsInstance(self.MyClassB.a1, UBInt8)
        self.assertIsInstance(self.MyClassB.a2, UBInt64)
        self.assertIsInstance(self.MyClassB.a4, UBInt16)
        self.assertIsInstance(self.MyClassB.a5, UBInt32)
        self.assertIsInstance(self.MyClassB.a0, UBInt32)
        self.assertIsInstance(self.MyClassB.b6, UBInt8)
