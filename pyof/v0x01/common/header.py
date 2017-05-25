"""Defines Header classes and related items."""

# System imports
from enum import IntEnum
from random import randint

# Local source tree imports
from pyof.foundation.base import GenericStruct
from pyof.foundation.basic_types import UBInt8, UBInt16, UBInt32
from pyof.foundation.constants import UBINT32_MAX_VALUE as MAXID
from pyof.v0x01.common.constants import OFP_VERSION

# Third-party imports

__all__ = ('Header', 'Type')

# Enums


class Type(IntEnum):
    """Enumeration of Message Types."""

    # Symetric/Immutable messages
    OFPT_HELLO = 0
    OFPT_ERROR = 1
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    OFPT_VENDOR = 4

    # Switch configuration messages
    # Controller/Switch messages
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_GET_CONFIG_REQUEST = 7
    OFPT_GET_CONFIG_REPLY = 8
    OFPT_SET_CONFIG = 9

    # Async messages
    OFPT_PACKET_IN = 10
    OFPT_FLOW_REMOVED = 11
    OFPT_PORT_STATUS = 12

    # Controller command messages
    # Controller/switch message
    OFPT_PACKET_OUT = 13
    OFPT_FLOW_MOD = 14
    OFPT_PORT_MOD = 15

    # Statistics messages
    # Controller/Switch message
    OFPT_STATS_REQUEST = 16
    OFPT_STATS_REPLY = 17

    # Barrier messages
    # Controller/Switch message
    OFPT_BARRIER_REQUEST = 18
    OFPT_BARRIER_REPLY = 19

    # Queue Configuration messages
    # Controller/Switch message
    OFPT_QUEUE_GET_CONFIG_REQUEST = 20
    OFPT_QUEUE_GET_CONFIG_REPLY = 21


# Classes


class Header(GenericStruct):
    """Representation of an OpenFlow message Header."""

    version = UBInt8(OFP_VERSION)
    message_type = UBInt8(enum_ref=Type)
    length = UBInt16()
    xid = UBInt32()

    def __init__(self, message_type=None, length=None, xid=None):
        """The constructor takes the optional parameters below.

        Args:
            message_type (~pyof.v0x01.common.header.Type): Type of the message.
            xid (int): ID of the message. Defaults to a random integer.
            length (int): Length of the message, including the header itself.
        """
        super().__init__()
        self.message_type = message_type
        self.length = length
        self.xid = randint(0, MAXID) if xid is None else xid
