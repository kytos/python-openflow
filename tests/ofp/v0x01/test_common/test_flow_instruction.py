import unittest
import sys
import os

# OFP Modules to be tested
sys.path.insert(0, os.path.abspath('.') + '/ofp/v0x01')
from common import flow_instruction

class TestFlowInstruction(unittest.TestCase):

    def test_method(self):
        print("Called FlowInstructionTest.test_method.")

sys.path.remove(os.path.abspath('.') + '/ofp/v0x01')
