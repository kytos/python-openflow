"""Defines common structures and enums for controller2switch."""

# System imports
from enum import IntEnum

from pyof.foundation.base import GenericMessage, GenericStruct
from pyof.foundation.basic_types import (
    Char, FixedTypeList, Pad, UBInt8, UBInt16, UBInt32, UBInt64)
from pyof.foundation.constants import OFP_MAX_TABLE_NAME_LEN
from pyof.v0x04.asynchronous.flow_removed import FlowRemovedReason
from pyof.v0x04.asynchronous.packet_in import PacketInReason
from pyof.v0x04.asynchronous.port_status import PortReason
# Local source tree imports
from pyof.v0x04.common.action import (
    ActionHeader, ControllerMaxLen, ListOfActions)
from pyof.v0x04.common.flow_instructions import ListOfInstruction
from pyof.v0x04.common.flow_match import ListOfOxmHeader
from pyof.v0x04.common.header import Header
from pyof.v0x04.controller2switch.table_mod import Table

__all__ = ('ConfigFlag', 'ControllerRole', 'Bucket', 'BucketCounter',
           'ExperimenterMultipartHeader', 'MultipartType',
           'TableFeaturePropType', 'Property', 'InstructionsProperty',
           'NextTablesProperty', 'ActionsProperty', 'OxmProperty',
           'ListOfProperty', 'TableFeatures')

# Enum


class ConfigFlag(IntEnum):
    """Handling of IP fragments."""

    #: No special handling for fragments.
    OFPC_FRAG_NORMAL = 0
    #: Drop fragments.
    OFPC_FRAG_DROP = 1
    #: Reassemble (only if OFPC_IP_REASM set).
    OFPC_FRAG_REASM = 2
    OFPC_FRAG_MASK = 3


class ControllerRole(IntEnum):
    """Controller roles."""

    #: Don’t change current role.
    OFPCR_ROLE_NOCHANGE = 0
    #: Default role, full access.
    OFPCR_ROLE_EQUAL = 1
    #: Full access, at most one master.
    OFPCR_ROLE_MASTER = 2
    #: Read-only access.
    OFPCR_ROLE_SLAVE = 3


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
        """Return a class related with this type."""
        if self.value <= 1:
            return InstructionsProperty
        elif self.value <= 3:
            return NextTablesProperty
        elif self.value <= 7:
            return ActionsProperty

        return OxmProperty


class MultipartType(IntEnum):
    """Types of Multipart Messages, both Request and Reply."""

    #: Description of this OpenFlow switch.
    #: The request body is empty.
    #: The reply body is struct ofp_desc.
    OFPMP_DESC = 0

    #: Individual flow statistics.
    #: The request body is struct ofp_flow_stats_request.
    #: The reply body is an array of struct ofp_flow_stats.
    OFPMP_FLOW = 1

    #: Aggregate flow statistics.
    #: The request body is struct ofp_aggregate_stats_request.
    #: The reply body is struct ofp_aggregate_stats_reply.
    OFPMP_AGGREGATE = 2

    #: Flow table statistics.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_table_stats.
    OFPMP_TABLE = 3

    #: Port statistics.
    #: The request body is struct ofp_port_stats_request.
    #: The reply body is an array of struct ofp_port_stats.
    OFPMP_PORT_STATS = 4

    #: Queue statistics for a port.
    #: The request body is struct ofp_queue_stats_request.
    #: The reply body is an array of struct ofp_queue_stats.
    OFPMP_QUEUE = 5

    #: Group counter statistics.
    #: The request body is struct ofp_group_stats_request.
    #: The reply is an array of struct ofp_group_stats.
    OFPMP_GROUP = 6

    #: Group description.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_group_desc_stats.
    OFPMP_GROUP_DESC = 7

    #: Group features.
    #: The request body is empty.
    #: The reply body is struct ofp_group_features.
    OFPMP_GROUP_FEATURES = 8

    #: Meter statistics.
    #: The request body is struct ofp_meter_multipart_requests.
    #: The reply body is an array of struct ofp_meter_stats.
    OFPMP_METER = 9

    #: Meter configuration.
    #: The request body is struct ofp_meter_multipart_requests.
    #: The reply body is an array of struct ofp_meter_config.
    OFPMP_METER_CONFIG = 10

    #: Meter features.
    #: The request body is empty.
    #: The reply body is struct ofp_meter_features.
    OFPMP_METER_FEATURES = 11

    #: Table features.
    #: The request body is either empty or contains an array of
    #: struct ofp_table_features containing the controller’s desired view of
    #: the switch. If the switch is unable to set the specified view an error
    #: is returned.
    #: The reply body is an array of struct ofp_table_features.
    OFPMP_TABLE_FEATURES = 12

    #: Port description.
    #: The request body is empty.
    #: The reply body is an array of struct ofp_port.
    OFPMP_PORT_DESC = 13

    #: Experimenter extension.
    #: The request and reply bodies begin with
    #: struct ofp_experimenter_multipart_header.
    #: The request and reply bodies are otherwise experimenter-defined.
    OFPMP_EXPERIMENTER = 0xffff


# Classes

class Bucket(GenericStruct):
    """Bucket for use in groups."""

    length = UBInt16()
    weight = UBInt16()
    watch_port = UBInt32()
    watch_group = UBInt32()
    pad = Pad(4)
    actions = FixedTypeList(ActionHeader)

    def __init__(self, length=None, weight=None, watch_port=None,
                 watch_group=None, actions=None):
        """Initialize all instance variables.

        Args:
            length (int): Length the bucket in bytes, including this header and
                any padding to make it 64-bit aligned.
            weight (int): Relative weight of bucket. Only defined for select
                groups.
            watch_port (int): Port whose state affects whether this bucket is
                live. Only required for fast failover groups.
            watch_group (int): Group whose state affects whether this bucket is
                live. Only required for fast failover groups.
            actions (~pyof.v0x04.common.action.ListOfActions): The action
                length is inferred from the length field in the header.
        """
        super().__init__()
        self.length = length
        self.weight = weight
        self.watch_port = watch_port
        self.watch_group = watch_group
        self.actions = actions


class BucketCounter(GenericStruct):
    """Used in group stats replies."""

    #: Number of packets processed by bucket.
    packet_count = UBInt64()
    #: Number of bytes processed by bucket.
    byte_count = UBInt64()

    def __init__(self, packet_count=None, byte_count=None):
        """Create BucketCounter with the optional parameters below.

        Args:
            packet_count (int): Number of packets processed by bucket.
            byte_count (int): Number of bytes processed by bucket.
        """
        super().__init__()
        self.packet_count = packet_count
        self.byte_count = byte_count


# Base Classes for other messages - not meant to be directly used, so, because
# of that, they will not be inserted on the __all__ attribute.


class AsyncConfig(GenericMessage):
    """Asynchronous message configuration base class.

    Common structure for SetAsync and GetAsyncReply messages.

    AsyncConfig contains three 2-element arrays. Each array controls whether
    the controller receives asynchronous messages with a specific
    :class:`~pyof.v0x04.common.header.Type`. Within each array, element
    0 specifies messages of interest when the controller has a OFPCR_ROLE_EQUAL
    or OFPCR_ROLE_MASTER role; element 1, when the controller has a
    OFPCR_ROLE_SLAVE role. Each array element is a bit-mask in which a 0-bit
    disables receiving a message sent with the reason code corresponding to the
    bit index and a 1-bit enables receiving it.
    """

    #: OpenFlow :class:`~pyof.v0x04.common.header.Header`
    #: OFPT_GET_ASYNC_REPLY or OFPT_SET_ASYNC.
    header = Header()
    packet_in_mask1 = UBInt32(enum_ref=PacketInReason)
    packet_in_mask2 = UBInt32(enum_ref=PacketInReason)
    port_status_mask1 = UBInt32(enum_ref=PortReason)
    port_status_mask2 = UBInt32(enum_ref=PortReason)
    flow_removed_mask1 = UBInt32(enum_ref=FlowRemovedReason)
    flow_removed_mask2 = UBInt32(enum_ref=FlowRemovedReason)

    def __init__(self, xid=None, packet_in_mask1=None, packet_in_mask2=None,
                 port_status_mask1=None, port_status_mask2=None,
                 flow_removed_mask1=None, flow_removed_mask2=None):
        """Create a AsyncConfig with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            packet_in_mask1
                (~pyof.v0x04.asynchronous.packet_in.PacketInReason):
                    A instance of PacketInReason
            packet_in_mask2
                (~pyof.v0x04.asynchronous.packet_in.PacketInReason):
                    A instance of PacketInReason
            port_status_mask1
                (~pyof.v0x04.asynchronous.port_status.PortReason):
                    A instance of PortReason
            port_status_mask2
                (~pyof.v0x04.asynchronous.port_status.PortReason):
                    A instance of PortReason
            flow_removed_mask1
                (~pyof.v0x04.asynchronous.flow_removed.FlowRemoved):
                    A instance of FlowRemoved.
            flow_removed_mask2
                (~pyof.v0x04.asynchronous.flow_removed.FlowRemoved):
                    A instance of FlowRemoved.
        """
        super().__init__(xid)
        self.packet_in_mask1 = packet_in_mask1
        self.packet_in_mask2 = packet_in_mask2
        self.port_status_mask1 = port_status_mask1
        self.port_status_mask2 = port_status_mask2
        self.flow_removed_mask1 = flow_removed_mask1
        self.flow_removed_mask2 = flow_removed_mask2


class RoleBaseMessage(GenericMessage):
    """Role basic structure for RoleRequest and RoleReply messages."""

    #: :class:`~pyof.v0x04.common.header.Header`
    #: Type OFPT_ROLE_REQUEST/OFPT_ROLE_REPLY.
    header = Header()
    #: One of NX_ROLE_*. (:class:`~.controller2switch.common.ControllerRole`)
    role = UBInt32(enum_ref=ControllerRole)
    #: Align to 64 bits.
    pad = Pad(4)
    #: Master Election Generation Id.
    generation_id = UBInt64()

    def __init__(self, xid=None, role=None, generation_id=None):
        """Create a RoleBaseMessage with the optional parameters below.

        Args:
            xid (int): OpenFlow xid to the header.
            role (:class:`~.controller2switch.common.ControllerRole`): .
            generation_id (int): Master Election Generation Id.
        """
        super().__init__(xid)
        self.role = role
        self.generation_id = generation_id


class SwitchConfig(GenericMessage):
    """Used as base class for SET_CONFIG and GET_CONFIG_REPLY messages."""

    #: OpenFlow :class:`~pyof.v0x04.common.header.Header`
    header = Header()
    flags = UBInt16(enum_ref=ConfigFlag)
    miss_send_len = UBInt16()

    def __init__(self, xid=None, flags=ConfigFlag.OFPC_FRAG_NORMAL,
                 miss_send_len=ControllerMaxLen.OFPCML_NO_BUFFER):
        """Create a SwitchConfig with the optional parameters below.

        Args:
            xid (int): xid to be used on the message header.
            flags (ConfigFlag): OFPC_* flags.
            miss_send_len (int): UBInt16 max bytes of new flow that the
                datapath should send to the controller.
        """
        super().__init__(xid)
        self.flags = flags
        self.miss_send_len = miss_send_len


# Multipart body

class ExperimenterMultipartHeader(GenericStruct):
    """Body for ofp_multipart_request/reply of type OFPMP_EXPERIMENTER."""

    experimenter = UBInt32()
    exp_type = UBInt32()
    #: Followed by experimenter-defined arbitrary data.

    def __init__(self, experimenter=None, exp_type=None):
        """Create a ExperimenterMultipartHeader with the parameters below.

        Args:
            experimenter: Experimenter ID which takes the same form as in
                struct ofp_experimenter_header (
                :class:`~pyof.v0x04.symmetric.experimenter.ExperimenterHeader`)
            exp_type: Experimenter defined.
        """
        super().__init__()
        self.experimenter = experimenter
        self.exp_type = exp_type


class Property(GenericStruct):
    """Table Property class.

    This class represents a Table Property generic structure.
    """

    property_type = UBInt16(enum_ref=TableFeaturePropType)
    length = UBInt16(4)

    def __init__(self, property_type=None):
        """Create a Property with the optional parameters below.

        Args:
            type(|TableFeaturePropType_v0x04|):
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
        """Create a InstructionsProperty with the optional parameters below.

        Args:
            type(|TableFeaturePropType_v0x04|):
                Property Type value of this instance.
            next_table_ids(|ListOfInstruction_v0x04|):
                List of InstructionGotoTable instances.
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
                 next_table_ids=None):
        """Create a NextTablesProperty with the optional parameters below.

        Args:
            type(|TableFeaturePropType_v0x04|):
                Property Type value of this instance.
            next_table_ids (|ListOfInstruction_v0x04|):
                List of InstructionGotoTable instances.
        """
        super().__init__(property_type)
        self.next_table_ids = (ListOfInstruction() if next_table_ids is None
                               else next_table_ids)
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
        """Create a ActionsProperty with the optional parameters below.

        Args:
            type(|TableFeaturePropType_v0x04|):
                Property Type value of this instance.
            action_ids(|ListOfActions_v0x04|):
                List of Action instances.
        """
        super().__init__(property_type)
        self.action_ids = action_ids if action_ids else ListOfActions()
        self.update_length()


class OxmProperty(Property):
    """Match, Wildcard or Set-Field property.

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
                 oxm_ids=None):
        """Create an OxmProperty with the optional parameters below.

        Args:
            type(|TableFeaturePropType_v0x04|):
                Property Type value of this instance.
            oxm_ids(|ListOfOxmHeader_v0x04|):
                List of OxmHeader instances.
        """
        super().__init__(property_type)
        self.oxm_ids = ListOfOxmHeader() if oxm_ids is None else oxm_ids
        self.update_length()


class ListOfProperty(FixedTypeList):
    """List of Table Property.

    Represented by instances of Property.
    """

    def __init__(self, items=None):
        """Create a ListOfProperty with the optional parameters below.

        Args:
            items (|Property_v0x04|): Instance or a list of instances.
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
                 properties=None):
        """Create a TableFeatures with the optional parameters below.

        Args:
            table_id(int): Indetifier of table.The default value
                OFPTT_ALL(``0xff``) will apply the configuration to all tables
                in the switch.
            name(Char): Characters representing the table name.
            metadata_match(int): Indicate the bits of the metadata field that
               the table can match on.The default value ``0xFFFFFFFFFFFFFFFF``
               indicates that the table can match the full metadata field.
            metadata_write(int): Indicates the bits of the metadata field that
               the table can write using the OFPIT_WRITE_METADATA instruction.
               The default value ``0xFFFFFFFFFFFFFFFF`` indicates that the
               table can write the full metadata field.
            config(int): Field reseved for future use.
            max_entries(int): Describe the maximum number of flow entries that
                can be inserted into that table.
            properties(~pyof.v0x04.controller2switch.common.ListOfProperty):
                List of Property intances.
        """
        super().__init__()
        self.table_id = table_id
        self.name = name
        self.metadata_match = metadata_match
        self.metadata_write = metadata_write
        self.config = config
        self.max_entries = max_entries
        self.properties = (ListOfProperty() if properties is None else
                           properties)
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
