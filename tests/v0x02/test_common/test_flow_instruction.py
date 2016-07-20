import unittest

from pyof.v0x02.common import flow_instruction


class TestOFPInstructionGoToTable(unittest.TestCase):
    def test_get_size(self):
        message = flow_instruction.OFPInstructionGoToTable(
                type=flow_instruction.OFPInstructionsType.OFPIT_GOTO_TABLE,
                len=8, table_id=1, pad=[0, 0, 0])
        self.assertEqual(message.get_size(), 8)

    def test_pack(self):
        message = flow_instruction.OFPInstructionGoToTable(
                type=flow_instruction.OFPInstructionsType.OFPIT_GOTO_TABLE,
                len=8, table_id=1, pad=[0, 0, 0])
        message.pack()

    def test_unpack(self):
        pass


class TestOFPInstructionWriteMetadata(unittest.TestCase):
    def test_get_size(self):
        message = flow_instruction.OFPInstructionWriteMetadata(
                type=flow_instruction.OFPInstructionsType.OFPIT_WRITE_METADATA,
                len=24, pad=[0, 0, 0, 0], metadata=1, metadata_mask=1)
        self.assertEqual(message.get_size(), 24)

    def test_pack(self):
        message = flow_instruction.OFPInstructionWriteMetadata(
                type=flow_instruction.OFPInstructionsType.OFPIT_WRITE_METADATA,
                len=24, pad=[0, 0, 0, 0], metadata=1, metadata_mask=1)
        message.pack()

    def test_unpack(self):
        pass


class TestOFPInstructionActions(unittest.TestCase):
    def test_get_size(self):
        message = flow_instruction.OFPInstructionActions(
            type=flow_instruction.OFPInstructionsType.OFPIT_WRITE_ACTIONS,
            len=8)
        self.assertEqual(message.get_size(), 8)

    def test_pack(self):
        message = flow_instruction.OFPInstructionActions(
            type=flow_instruction.OFPInstructionsType.OFPIT_WRITE_ACTIONS,
            len=8)
        message.pack()

    def test_unpack(self):
        pass
