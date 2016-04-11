"""Defines flows instructions associated with a flow table entry."""

# System imports
import enum

# Third-party imports

# Local source tree imports
from common import action
from foundation import base
from foundation import basic_types

# Enums


class OFPInstructionsType (enum.Enum):
    """
    Defines types of instructions.
    Enums:
        OFPIT_GOTO_TABLE        # Setup next table in the lookup pipeline
        OFPIT_WRITE_METADATA    # Setup the metadata for use later in pipeline
        OFPIT_WRITE_ACTIONS     # Write the action(s) onto the datapath set
        OFPIT_APPLY_ACTIONS     # Applies the actio(s) immediately
        OFPIT_CLEAR_ACTIONS     # Clears all actions from the datapath
        OFPIT_EXPERIMENTER      # Experimenter instruction


    """
    OFPIT_GOTO_TABLE = 1
    OFPIT_WRITE_METADATA = 2
    OFPIT_WRITE_ACTIONS = 3
    OFPIT_APPLY_ACTIONS = 4
    OFPIT_CLEAR_ACTIONS = 5
    OFPIT_EXPERIMENTER = 0xFFF


# Classes


class OFPInstructionGoToTable (base.GenericStruct):
    """
    WriteMetadata Classe uses this to process pipeline.
    """
    type = basic_types.UBInt16()
    len = basic_types.UBInt16()
    table_id = basic_types.UBInt8()
    pad = basic_types.UBInt8Array(length=3)


class OFPInstructionWriteMetadata (base.GenericStruct):
    """
    Metadata for the next table lookup.
    """
    type = basic_types.UBInt16()
    len = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=4)
    metadata = basic_types.UBInt64()
    metadata_mask = basic_types.UBInt64


class OFPInstructionActions (base.GenericStruct):
    """
    List of actions that are applied to the packet packet-in.
    """
    type = basic_types.UBInt16()
    len = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=4)
    actions = action.OFPActionStructure()
