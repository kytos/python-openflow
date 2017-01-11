"""Testing class inheritance attributes changes."""
import unittest

import pyof
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

            _remove_attributes = ['a3']
            _rename_attributes = [('a4', 'b4')]
            _insert_attributes_before = {'a0': 'a1'}

        self.MyClassA = MyClassA
        self.MyClassB = MyClassB
        self.a_expected_names = ['a1', 'a2', 'a3', 'a4', 'a5']
        self.b_expected_names = ['a0', 'a1', 'a2', 'b4', 'a5', 'b6']

    def test_modifications(self):
        """[Foundation/Base/GenericStruct] - Attributes Modifications."""
        # Checking keys (attributes names) and its ordering
        self.assertEqual(list(self.MyClassA.__ordered__.keys()),
                         self.a_expected_names)
        self.assertEqual(list(self.MyClassB.__ordered__.keys()),
                         self.b_expected_names)

        # Check if there is no shared attribute between instances
        m1 = self.MyClassA()
        m2 = self.MyClassB()
        self.assertIsNot(m1, m2)
        self.assertIsNot(m1.a1, m2.a0)
        self.assertIsNot(m1.a1, m2.a1)
        self.assertIsNot(m1.a2, m2.a2)
        self.assertIsNot(m1.a4, m2.b4)
        self.assertIsNot(m1.a5, m2.a5)

        # Check attributes types on MyClassA
        self.assertIs(self.MyClassA.__ordered__['a1'], UBInt8)
        self.assertIs(self.MyClassA.__ordered__['a2'], UBInt16)
        self.assertIs(self.MyClassA.__ordered__['a3'], UBInt8)
        self.assertIs(self.MyClassA.__ordered__['a4'], UBInt16)
        self.assertIs(self.MyClassA.__ordered__['a5'], UBInt32)

        # Check attributes types on MyClassA
        self.assertIs(self.MyClassB.__ordered__['a0'], UBInt32)
        self.assertIs(self.MyClassB.__ordered__['a1'], UBInt8)
        self.assertIs(self.MyClassB.__ordered__['a2'], UBInt64)
        self.assertIs(self.MyClassB.__ordered__['b4'], UBInt16)
        self.assertIs(self.MyClassB.__ordered__['a5'], UBInt32)
        self.assertIs(self.MyClassB.__ordered__['b6'], UBInt8)
