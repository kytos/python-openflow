"""Flow instructions to be executed.

The flow instructions associated with a flow table entry are executed when a
flow matches the entry.
"""
# System imports
from enum import Enum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import Pad, UBInt8, UBInt16, UBInt32, UBInt64
from pyof.v0x04.common.action import ListOfActions

# Third-party imports


__all__ = ('InstructionApplyAction', 'InstructionClearAction',
           'InstructionGotoTable', 'InstructionMeter', 'InstructionType',
           'InstructionWriteAction', 'InstructionWriteMetadata')

# Enums


class InstructionType(Enum):
    """List of instructions that are currently defined."""

    #: Setup the next table in the lookup pipeline
    OFPIT_GOTO_TABLE = 1
    #: Setup the metadata field for use later in pipeline
    OFPIT_WRITE_METADATA = 2
    #: Write the action(s) onto the datapath action set
    OFPIT_WRITE_ACTIONS = 3
    #: Applies the action(s) immediately
    OFPIT_APPLY_ACTIONS = 4
    #: Clears all actions from the datapath action set
    OFPIT_CLEAR_ACTIONS = 5
    #: Apply meter (rate limiter)
    OFPIT_METER = 6
    #: Experimenter instruction
    OFPIT_EXPERIMENTER = 0xFFFF


# Classes


class InstructionApplyAction(GenericStruct):
    """Instruction structure for OFPIT_APPLY_ACTIONS.

    The :attr:`~actions` field is treated as a list, and the actions are
    applied to the packet in-order.
    """

    #: OFPIT_APPLY_ACTIONS
    instruction_type = UBInt16(InstructionType.OFPIT_APPLY_ACTIONS,
                               enum_ref=InstructionType)
    #: Length of this struct in bytes.
    length = UBInt16()
    #: Align to 64-bits
    pad = Pad(4)
    #: Actions associated with OFPIT_APPLY_ACTIONS
    actions = ListOfActions()

    def __init__(self, length=None, actions=None):
        """Instruction structure for OFPIT_APPLY_ACTIONS.

        Args:
            - length (int): Length of this struct in bytes.
            - actions (:class:`~.actions.ListOfActions`): Actions associated
                with OFPIT_APPLY_ACTIONS.
        """
        super().__init__()
        self.length = length
        self.actions = actions if actions is not None else []


class InstructionClearAction(GenericStruct):
    """Instruction structure for OFPIT_CLEAR_ACTIONS.

    This structure does not contain any actions.
    """

    #: OFPIT_CLEAR_ACTIONS
    instruction_type = UBInt16(InstructionType.OFPIT_CLEAR_ACTIONS,
                               enum_ref=InstructionType)
    #: Length of this struct in bytes.
    length = UBInt16(8)
    #: Align to 64-bits
    pad = Pad(4)
    #: OFPIT_CLEAR_ACTIONS does not have any action on the list of actions.
    actions = ListOfActions()


class InstructionGotoTable(GenericStruct):
    """Instruction structure for OFPIT_GOTO_TABLE."""

    #: OFPIT_GOTO_TABLE.
    instruction_type = UBInt16(InstructionType.OFPIT_GOTO_TABLE,
                               enum_ref=InstructionType)
    #: Length of this struct in bytes.
    length = UBInt16()
    #: Set next table in the lookup pipeline.
    table_id = UBInt8()
    #: Pad to 64 bits.
    pad = Pad(3)

    def __init__(self, length=None, table_id=None):
        """Instruction structure for OFPIT_GOTO_TABLE.

        Args:
            - length (int): Length of this struct in bytes.
            - table_id (int): set next table in the lookup pipeline.
        """
        super().__init__()
        self.length = length
        self.table_id = table_id


class InstructionMeter(GenericStruct):
    """Instruction structure for OFPIT_METER.

    meter_id indicates which meter to apply on the packet.
    """

    #: OFPIT_METER.
    instruction_type = UBInt16(InstructionType.OFPIT_METER,
                               enum_ref=InstructionType)
    #: Length is 8.
    length = UBInt16(8)
    #: Meter instance.
    meter_id = UBInt32()

    def __init__(self, meter_id=None):
        """Instruction structure for OFPIT_METER.

        Args:
            - meter_id (int): Meter instance.
        """
        super().__init__()
        self.meter_id = meter_id


class InstructionWriteAction(GenericStruct):
    """Instruction structure for OFPIT_WRITE_ACTIONS.

    The actions field must be treated as a SET, so the actions are not
    repeated.
    """

    #: OFPIT_WRITE_ACTIONS
    instruction_type = UBInt16(InstructionType.OFPIT_WRITE_ACTIONS,
                               enum_ref=InstructionType)
    #: Length of this struct in bytes.
    length = UBInt16()
    #: Align to 64-bits
    pad = Pad(4)
    #: Actions associated with OFPIT_WRITE_ACTIONS
    actions = ListOfActions()

    def __init__(self, length=None, actions=None):
        """Instruction structure for OFPIT_WRITE_ACTIONS.

        Args:
            - length (int): Length of this struct in bytes.
            - actions (:class:`~.actions.ListOfActions`): Actions associated
                with OFPIT_WRITE_ACTIONS.
        """
        super().__init__()
        self.length = length
        self.actions = actions if actions is not None else []


class InstructionWriteMetadata(GenericStruct):
    """Instruction structure for OFPIT_WRITE_METADATA."""

    #: OFPIT_WRITE_METADATA
    instruction_type = UBInt16(InstructionType.OFPIT_WRITE_METADATA,
                               enum_ref=InstructionType)
    #: Length of this struct in bytes
    length = UBInt16()
    #: Align to 64-bits
    pad = Pad(4)
    #: Metadata value to write
    metadata = UBInt64()
    #: Metadata write bitmask
    metadata_mask = UBInt64()

    def __init__(self, length=None, metadata=None, metadata_mask=None):
        """Instruction structure for OFPIT_WRITE_METADATA.

        Args:
            - length (int): Length of this struct in bytes.
            - metadata (int): Metadata value to write.
            - metadata_mask (int): Metadata write bitmask.
        """
        super().__init__()
        self.length = length
        self.metadata = metadata
        self.metadata_mask = metadata_mask
