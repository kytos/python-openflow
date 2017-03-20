"""Test of v0x04 table_feature module."""

from pyof.v0x04.common.flow_instructions import (InstructionApplyAction,
                                                 InstructionClearAction)
from pyof.v0x04.common.table_feature import (InstructionsProperty,
                                             ListOfProperty, TableFeatures)
from pyof.v0x04.controller2switch.multipart_reply import (MultipartReply,
                                                          MultipartReplyFlags,
                                                          MultipartTypes)

from tests.v0x04.test_struct import TestStruct


class TestTableFeatures(TestStruct):
    """Class used to test TableFeatures structures."""

    @classmethod
    def setUpClass(cls):
        """Configure raw file and its object in parent class (TestDump)."""
        super().setUpClass()
        super().set_message(MultipartReply, xid=16,
                            multipart_type=MultipartTypes.OFPMP_TABLE_FEATURES,
                            flags=MultipartReplyFlags.OFPMPF_REPLY_MORE,
                            body=cls.table_features_instance())
        super().set_minimum_size(16)

    @classmethod
    def table_features_instance(cls):
        """Method used to create a TableFeature instance."""
        return TableFeatures(table_id=0, name="",
                             metadata_match=0xFFFFFFFFFFFFFFFF,
                             metadata_write=0xFFFFFFFFFFFFFFFF,
                             config=0, max_entries=0,
                             properties=cls.property_list())

    @staticmethod
    def property_list():
        """Method used to instantiate a ListOfProperty with some instances."""
        instructions = [InstructionApplyAction(), InstructionClearAction()]
        ip = InstructionsProperty(instruction_ids=instructions)
        return ListOfProperty(items=[ip])
