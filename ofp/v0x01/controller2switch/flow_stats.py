"""Body of the reply to an OFPST_FLOW"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.common import flow_match
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types

# Classes


class FlowStats(base.GenericStruct):
    """
    Body of reply to OFPST_FLOW request.

        :param length:        Length of this entry
        :param table_id:      ID of table flow came from
        :param pad:           Align to 32 bits
        :param match:         Description of fields
        :param duration_sec:  Time flow has been alive in seconds
        :param duration_nsec: Time flow has been alive in nanoseconds beyond
                              duration_sec
        :param priority:      Priority of the entry. Only meaningful when this
                              is not an exact-match entry
        :param idle_timeout:  Number of seconds idle before expiration
        :param hard_timeout:  Number of seconds before expiration
        :param pad2:          Align to 64-bits
        :param cookie:        Opaque controller-issued identifier
        :param packet_count:  Number of packets in flow
        :param byte_count:    Number of bytes in flow
        :param actions:       Actions
    """
    length = basic_types.UBInt16()
    table_id = basic_types.UBInt8()
    pad = basic_types.PAD(1)
    match = flow_match.Match()
    duration_sec = basic_types.UBInt32()
    duration_nsec = basic_types.UBInt32()
    priority = basic_types.UBInt16()
    idle_timeout = basic_types.UBInt16()
    hard_timeout = basic_types.UBInt16()
    pad2 = basic_types.PAD(6)
    cookie = basic_types.UBInt64()
    packet_count = basic_types.UBInt64()
    byte_count = basic_types.UBInt64()
    # actions = basic_types.UBInt8Array(length=0)
    actions = []
    # TODO: Add here a new type, list of ActionHeaders()
    #       objects. Related to ISSUE #3

    def __init__(self, length=None, table_id=None, match=None,
                 duration_sec=None, duration_nsec=None, priority=None,
                 idle_timeout=None, hard_timeout=None, cookie=None,
                 packet_count=None, byte_count=None, actions=None):

        self.length = length
        self.table_id = table_id
        if match is not None:
            self.match = match
        self.duration_sec = duration_sec
        self.duration_nsec = duration_nsec
        self.prioriry = priority
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.cookie = cookie
        self.packet_count = packet_count
        self.byte_count = byte_count
        if actions is not None:
            self.actions = actions
