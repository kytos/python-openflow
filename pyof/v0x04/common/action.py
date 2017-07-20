"""Defines actions that may be associated with flows packets."""
# System imports
from enum import IntEnum

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import (
    FixedTypeList, Pad, UBInt8, UBInt16, UBInt32)
from pyof.v0x04.common.flow_match import OxmTLV

# Third-party imports

__all__ = ('ActionExperimenterHeader', 'ActionGroup', 'ActionHeader',
           'ActionMPLSTTL', 'ActionNWTTL', 'ActionOutput', 'ActionPopMPLS',
           'ActionPush', 'ActionSetField', 'ActionSetQueue', 'ActionType',
           'ControllerMaxLen', 'ListOfActions')

# Enums


class ActionType(IntEnum):
    """Actions associated with flows and packets."""

    #: Output to switch port.
    OFPAT_OUTPUT = 0
    #: Copy TTL "outwards" -- from next-to-outermost to outermost
    OFPAT_COPY_TTL_OUT = 11
    #: Copy TTL "inwards" -- from outermost to next-to-outermost
    OFPAT_COPY_TTL_IN = 12
    #: MPLS TTL
    OFPAT_SET_MPLS_TTL = 15
    #: Decrement MPLS TTL
    OFPAT_DEC_MPLS_TTL = 16
    #: Push a new VLAN tag
    OFPAT_PUSH_VLAN = 17
    #: Pop the outer VLAN tag
    OFPAT_POP_VLAN = 18
    #: Push a new MPLS tag
    OFPAT_PUSH_MPLS = 19
    #: Pop the outer MPLS tag
    OFPAT_POP_MPLS = 20
    #: Set queue id when outputting to a port
    OFPAT_SET_QUEUE = 21
    #: Apply group.
    OFPAT_GROUP = 22
    #: IP TTL.
    OFPAT_SET_NW_TTL = 23
    #: Decrement IP TTL.
    OFPAT_DEC_NW_TTL = 24
    #: Set a header field using OXM TLV format.
    OFPAT_SET_FIELD = 25
    #: Push a new PBB service tag (I-TAG)
    OFPAT_PUSH_PBB = 26
    #: Pop the outer PBB service tag (I-TAG)
    OFPAT_POP_PBB = 27
    #: Experimenter type
    OFPAT_EXPERIMENTER = 0xffff


class ControllerMaxLen(IntEnum):
    """A max_len of OFPCML_NO_BUFFER means not to buffer.

    The packet should be sent.
    """

    #: maximum max_len value which can be used to request a specific byte
    #:     length.
    OFPCML_MAX = 0xffe5
    #: indicates that no buffering should be applied and the whole packet is to
    #:     be sent to the controller.
    OFPCML_NO_BUFFER = 0xffff


# Classes


class ActionExperimenterHeader(GenericStruct):
    """Action structure for OFPAT_EXPERIMENTER."""

    #: OFPAT_EXPERIMENTER.
    action_type = UBInt16(ActionType.OFPAT_EXPERIMENTER, enum_ref=ActionType)
    #: Length is multiple of 8.
    length = UBInt16()
    #: Experimenter ID which takes the same form as in struct
    #:     ofp_experimenter_header
    experimenter = UBInt32()

    def __init__(self, length=None, experimenter=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            experimenter (int): The experimenter field is the Experimenter ID,
                which takes the same form as in struct ofp_experimenter.
        """
        super().__init__()
        self.length = length
        self.experimenter = experimenter


class ActionGroup(GenericStruct):
    """Action structure for OFPAT_GROUP."""

    #: OFPAT_GROUP.
    action_type = UBInt16(ActionType.OFPAT_GROUP, enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: Group identifier.
    group_id = UBInt32()

    def __init__(self, group_id=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            group_id (int): The group_id indicates the group used to process
                this packet. The set of buckets to apply depends on the group
                type.
        """
        super().__init__()
        self.group_id = group_id


class ActionHeader(GenericStruct):
    """Action header that is common to all actions.

    The length includes the header and any padding used to make the action
    64-bit aligned.
    NB: The length of an action *must* always be a multiple of eight.
    """

    #: One of OFPAT_*.
    action_type = UBInt16(enum_ref=ActionType)
    #: Length of action, including this header. This is the length of actions,
    #:    including any padding to make it 64-bit aligned.
    length = UBInt16()
    #: Pad for 64-bit alignment.
    pad = Pad(4)

    def __init__(self, action_type=None, length=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            action_type (~pyof.v0x04.common.action.ActionType):
                The type of the action.
            length (int): Length of action, including this header.
        """
        super().__init__()
        self.action_type = action_type
        self.length = length


class ActionMPLSTTL(GenericStruct):
    """Action structure for OFPAT_SET_MPLS_TTL."""

    #: OFPAT_SET_MPLS_TTL.
    action_type = UBInt16(ActionType.OFPAT_SET_MPLS_TTL, enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: MPLS TTL
    mpls_ttl = UBInt8()
    #: Padding
    pad = Pad(3)

    def __init__(self, mpls_ttl=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            mpls_ttl (int): The mpls_ttl field is the MPLS TTL to set.
        """
        super().__init__()
        self.mpls_ttl = mpls_ttl


class ActionNWTTL(GenericStruct):
    """Action structure for OFPAT_SET_NW_TTL."""

    #: OFPAT_SET_NW_TTL.
    action_type = UBInt16(ActionType.OFPAT_SET_NW_TTL, enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: IP TTL
    nw_ttl = UBInt8()
    #: Padding
    pad = Pad(3)

    def __init__(self, nw_ttl=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            nw_ttl (int): the TTL address to set in the IP header.
        """
        super().__init__()
        self.nw_ttl = nw_ttl


class ActionOutput(GenericStruct):
    """Defines the actions output.

    Action structure for :attr:`ActionType.OFPAT_OUTPUT`, which sends packets
    out :attr:`port`. When the :attr:`port` is the
    :attr:`.Port.OFPP_CONTROLLER`, :attr:`max_length` indicates the max number
    of bytes to send. A :attr:`max_length` of zero means no bytes of the packet
    should be sent.
    """

    #: OFPAT_OUTPUT.
    action_type = UBInt16(ActionType.OFPAT_OUTPUT, enum_ref=ActionType)
    #: Length is 16.
    length = UBInt16(16)
    #: Output port.
    port = UBInt16()
    #: Max length to send to controller.
    max_length = UBInt16()
    #: Pad to 64 bits.
    pad = Pad(6)

    def __init__(self, action_type=None, length=None, port=None,
                 max_length=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            port (:class:`Port` or :class:`int`): Output port.
            max_length (int): Max length to send to controller.
        """
        super().__init__()
        self.action_type = action_type
        self.length = length
        self.port = port
        self.max_length = max_length


class ActionPopMPLS(GenericStruct):
    """Action structure for OFPAT_POP_MPLS."""

    #: OFPAT_POP_MPLS.
    action_type = UBInt16(ActionType.OFPAT_POP_MPLS, enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: Ethertype
    ethertype = UBInt16()
    #: Padding
    pad = Pad(2)

    def __init__(self, ethertype=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            ethertype (int): indicates the Ethertype of the payload.
        """
        super().__init__()
        self.ethertype = ethertype


class ActionPush(GenericStruct):
    """Action structure for OFPAT_PUSH_VLAN/MPLS/PBB."""

    #: OFPAT_PUSH_VLAN/MPLS/PBB.
    action_type = UBInt16(enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: Ethertype
    ethertype = UBInt16()
    #: Padding
    pad = Pad(2)

    def __init__(self, ethertype=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            ethertype (int): indicates the Ethertype of the new tag.
        """
        super().__init__()
        self.ethertype = ethertype


class ActionSetField(GenericStruct):
    """Action structure for OFPAT_SET_FIELD."""

    #: OFPAT_SET_FIELD.
    action_type = UBInt16(ActionType.OFPAT_SET_FIELD, enum_ref=ActionType)
    #: Length is padded to 64 bits.
    length = UBInt16()
    pad = Pad(length=4)
    #: OXM TLV - Make compiler happy
    field = OxmTLV()

    def __init__(self, length=None, field=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            length (int): length padded to 64 bits, followed by exactly
                          oxm_len bytes containing a single OXM TLV, then
                          exactly ((oxm_len + 4) + 7)/8*8 - (oxm_len + 4)
                          (between 0 and 7) bytes of all-zero bytes
            field  (OcmTLV): OXM field.
        """
        super().__init__()
        self.length = length
        self.field = field

    def _get_size(self):
        super_size = super()._get_size()
        return super_size + (8 - (super_size % 8)) % 8

    def _update_length(self):
        self.length = self._get_size()

    def _pack(self):
        self._update_length()
        packet = super()._pack()
        super_size = len(packet)
        lacking_bytes = self._get_size() - super_size
        if lacking_bytes != 0:
            packet += Pad(lacking_bytes).pack()
        return packet


class ActionSetQueue(GenericStruct):
    """Action structure for OFPAT_SET_QUEUE."""

    #: OFPAT_SET_QUEUE.
    action_type = UBInt16(ActionType.OFPAT_SET_QUEUE, enum_ref=ActionType)
    #: Length is 8.
    length = UBInt16(8)
    #: Queue id for the packets.
    queue_id = UBInt32()

    def __init__(self, queue_id=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            queue_id (int): The queue_id send packets to given queue on port.
        """
        super().__init__()
        self.queue_id = queue_id


class ListOfActions(FixedTypeList):
    """List of actions.

    Represented by instances of ActionHeader and used on ActionHeader objects.
    """

    def __init__(self, items=None):
        """The constructor just assigns parameters to object attributes.

        Args:
            items (~pyof.v0x04.common.action.ActionHeader):
                Instance or a list of instances.
        """
        super().__init__(pyof_class=ActionHeader, items=items)
