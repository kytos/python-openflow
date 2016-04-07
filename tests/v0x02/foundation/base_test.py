import unittest
import sys

# OFP Modules to be tested
from ofp.v0x02.foundation.base import GenericType

class BaseTest(unittest.TestCase):

    def test_pack(self):
        genericType = GenericType()

if __name__ == "__main__":
    unittest.main()
