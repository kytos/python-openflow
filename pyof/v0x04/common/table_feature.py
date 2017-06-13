"""Table Features and releated enum.

This module contains the Table Features struture and your Property types.
"""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    Char, FixedTypeList, Pad, UBInt8, UBInt16, UBInt32, UBInt64)
# Local source tree imports
from pyof.foundation.constants import OFP_MAX_TABLE_NAME_LEN
from pyof.v0x04.common.action import ListOfActions
from pyof.v0x04.common.flow_instructions import ListOfInstruction
from pyof.v0x04.common.flow_match import ListOfOxmHeader
from pyof.v0x04.controller2switch.table_mod import Table

__all__ = ('TableFeaturePropType', 'Property', 'InstructionsProperty',
           'NextTablesProperty', 'ActionsProperty', 'OxmProperty',
           'ListOfProperty', 'TableFeatures')


class TableFeaturePropType(IntEnum):
    """Table Property Types.

    Low order bit cleared indicates a property for a regular Flow Entry.
    Low order bit set indicates a property for the Table-Miss Flow Entry.
    """

    # Instructions property.
    OFPTFPT_INSTRUCTIONS = 0
    # Instructions for table-miss.
    OFPTFPT_INSTRUCTIONS_MISS = 1
    # Next Table property.
    OFPTFPT_NEXT_TABLES = 2
    # Next Table for table-miss.
    OFPTFPT_NEXT_TABLES_MISS = 3
    # Write Actions property.
    OFPTFPT_WRITE_ACTIONS = 4
    # Write Actions for table-miss.
    OFPTFPT_WRITE_ACTIONS_MISS = 5
    # Apply Actions property.
    OFPTFPT_APPLY_ACTIONS = 6
    # Apply Actions for table-miss.
    OFPTFPT_APPLY_ACTIONS_MISS = 7
    # Match property.
    OFPTFPT_MATCH = 8
    # Wildcards property.
    OFPTFPT_WILDCARDS = 10
    # Write Set-Field property.
    OFPTFPT_WRITE_SETFIELD = 12
    # Write Set-Field for table-miss.
    OFPTFPT_WRITE_SETFIELD_MISS = 13
    # Apply Set-Field property.
    OFPTFPT_APPLY_SETFIELD = 14
    # Apply Set-Field for table-miss.
    OFPTFPT_APPLY_SETFIELD_MISS = 15
    # Experimenter property.
    OFPTFPT_EXPERIMENTER = 0xFFFE
    # Experimenter for table-miss.
    OFPTFPT_EXPERIMENTER_MISS = 0xFFFF

    def find_class(self):
        """Method used to return a class related with this type."""
        if self.value <= 1:
            return InstructionsProperty
        elif self.value <= 3:
            return NextTablesProperty
        elif self.value <= 7:
            return ActionsProperty

        return OxmProperty


# Classes


class Property(GenericStruct):
    """Table Property class.

    This class represents a Table Property generic structure.
    """

    property_type = UBInt16(enum_ref=TableFeaturePropType)
    length = UBInt16(4)

    def __init__(self, property_type=None):
        """Constructor of Generic Instruction receives the parameters bellow.

        Args:
            type(~pyof.v0x04.controller2switch.common.TableFeaturePropType):
                Property Type value of this instance.
        """
        super().__init__()
        self.property_type = property_type

    def pack(self, value=None):
        """Pack method used to update the length of instance and  packing.

        Args:
            value: Structure to be packed.
        """
        self.update_length()
        return super().pack(value)

    def unpack(self, buff=None, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.
        """
        property_type = UBInt16(enum_ref=TableFeaturePropType)
        property_type.unpack(buff, offset)
        self.__class__ = TableFeaturePropType(property_type.value).find_class()

        length = UBInt16()
        length.unpack(buff, offset=offset+2)
        super().unpack(buff[:offset+length.value], offset=offset)

    def update_length(self):
        """Update the length of current instance."""
        self.length = self.get_size()


class InstructionsProperty(Property):
    """Instructions property.

    This class represents Property with the following types:
        OFPTFPT_INSTRUCTIONS
        OFPTFPT_INSTRUCTIONS_MISS
    """

    instruction_ids = ListOfInstruction()

    def __init__(self, property_type=TableFeaturePropType.OFPTFPT_INSTRUCTIONS,
                 instruction_ids=None):
        """Constructor of InstructionProperty receives the parameters bellow.

        Args:
            type(~pyof.v0x04.controller2switch.common.TableFeaturePropType):
                Property Type value of this instance.
            instruction_ids(ListOfInstruction): List of Instruction instances.
        """
        super().__init__(property_type=property_type)
        self.instruction_ids = instruction_ids if instruction_ids else []
        self.update_length()


class NextTablesProperty(Property):
    """Next Tables Property.

    This class represents Property with the following types:
        OFPTFPT_NEXT_TABLES
        OFPTFPT_NEXT_TABLES_MISS
    """

    next_table_ids = ListOfInstruction()

    def __init__(self, property_type=TableFeaturePropType.OFPTFPT_NEXT_TABLES,
                 next_table_ids=ListOfInstruction()):
        """Constructor of NextTablesProperty receives the parameters bellow.

        Args:
            type(~pyof.v0x04.controller2switch.common.TableFeaturePropType):
                Property Type value of this instance.
            next_table_ids(ListOfInstruction): List of InstructionGotoTable
                                               instances.
        """
        super().__init__(property_type)
        self.next_table_ids = next_table_ids
        self.update_length()


class ActionsProperty(Property):
    """Actions Property.

    This class represents Property with the following type:
        OFPTFPT_WRITE_ACTIONS
        OFPTFPT_WRITE_ACTIONS_MISS
        OFPTFPT_APPLY_ACTIONS
        OFPTFPT_APPLY_ACTIONS_MISS
    """

    action_ids = ListOfActions()

    def __init__(self,
                 property_type=TableFeaturePropType.OFPTFPT_WRITE_ACTIONS,
                 action_ids=None):
        """Constructor of ActionsProperty receives the parameters bellow.

        Args:
            type(~pyof.v0x04.controller2switch.common.TableFeaturePr):
                Property Type value of this instance.
            action_ids(ListOfActions): List of Action instances.
        """
        super().__init__(property_type)
        self.action_ids = action_ids if action_ids else ListOfActions()
        self.update_length()


class OxmProperty(Property):
    """"Match, Wildcard or Set-Field property.

    This class represents Property with the following types:
        OFPTFPT_MATCH
        OFPTFPT_WILDCARDS
        OFPTFPT_WRITE_SETFIELD
        OFPTFPT_WRITE_SETFIELD_MISS
        OFPTFPT_APPLY_SETFIELD
        OFPTFPT_APPLY_SETFIELD_MISS
    """

    oxm_ids = ListOfOxmHeader()

    def __init__(self, property_type=TableFeaturePropType.OFPTFPT_MATCH,
                 oxm_ids=ListOfOxmHeader()):
        """Constructor of OxmProperty receives the parameters bellow.

        Args:
            type(~pyof.v0x04.controller2switch.common.TableFeaturePropType):
                Property Type value of this instance.
            oxm_ids(~pyof.v0x04.common.flow_match.ListOfOxmHeader):
                List of OxmHeader instances.
        """
        super().__init__(property_type)
        self.oxm_ids = oxm_ids
        self.update_length()


class ListOfProperty(FixedTypeList):
    """List of Table Property.

    Represented by instances of Property.
    """

    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (~pyof.v0x04.controller2switch.common.Property):
                Instance or a list of instances.
        """
        super().__init__(pyof_class=Property, items=items)


class TableFeatures(GenericStruct):
    """Abstration of common class Table Features.

    Body for MultipartRequest of type OFPMP_TABLE_FEATURES.
    Body of reply to OFPMP_TABLE_FEATURES request.
    """

    length = UBInt16()
    # /* Identifier of table.  Lower numbered tables are consulted first. */
    table_id = UBInt8()
    # /* Align to 64-bits. */
    pad = Pad(5)
    name = Char(length=OFP_MAX_TABLE_NAME_LEN)
    # /* Bits of metadata table can match. */
    metadata_match = UBInt64()
    # /* Bits of metadata table can write. */
    metadata_write = UBInt64()
    # /* Bitmap of OFPTC_* values */
    config = UBInt32()
    # /* Max number of entries supported. */
    max_entries = UBInt32()
    # /* Table Feature Property list */
    properties = ListOfProperty()

    def __init__(self, table_id=Table.OFPTT_ALL, name="",
                 metadata_match=0xFFFFFFFFFFFFFFFF,
                 metadata_write=0xFFFFFFFFFFFFFFFF,
                 config=0,
                 max_entries=0,
                 properties=ListOfProperty()):
        """The constructor of TableFeatures receives the paramters below.

        Args:
            table_id(int): Indetifier of table.The default value
               OFPTT_ALL(0xff) will apply the configuration to all tables in
               the switch.
            name(Char): Characters representing the table name.
            metadata_match(int): Indicate the bits of the metadata field that
                the table can match on.The default value 0xFFFFFFFFFFFFFFFF
                indicates that the table can match the full metadata field.
            metadata_write(int): Indicates the bits of the metadata field that
               the table can write using the OFPIT_WRITE_METADATA instruction.
               The default value 0xFFFFFFFFFFFFFFFF indicates that the table
               can write the full metadata field.
            config(int): Field reseved for future use.
            max_entries(int): Describe the maximum number of flow entries that
               can be inserted into that table.
            properties(~pyof.v0x04.controller2switch.common.Property):
               List of Property intances.
        """
        super().__init__()
        self.table_id = table_id
        self.name = name
        self.metadata_match = metadata_match
        self.metadata_write = metadata_write
        self.config = config
        self.max_entries = max_entries
        self.properties = properties
        self.update_length()

    def pack(self, value=None):
        """Pack method used to update the length of instance and packing.

        Args:
            value: Structure to be packed.
        """
        self.update_length()
        return super().pack(value)

    def update_length(self):
        """Update the length of current instance."""
        self.length = self.get_size()

    def unpack(self, buff=None, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.
        """
        length = UBInt16()
        length.unpack(buff, offset)
        super().unpack(buff[:offset+length.value], offset)
