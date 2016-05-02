"""Information about tables is requested with OFPST_TABLE stats request type"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types


class TableStats(base.GenericStruct):
    """
    Body of reply to OFPST_TABLE request

        :param table_id:      Identifier of table.  Lower numbered tables
                              are consulted first
        :param pad:           Align to 32-bits
        :param name:          Table name
        :param wildcards:     Bitmap of OFPFW_* wildcards that are supported
                              by the table
        :param max_entries:   Max number of entries supported
        :param active_count:  Number of active entries
        :param count_lookup:  Number of packets looked up in table
        :param count_matched: Number of packets that hit table
    """
    table_id = basic_types.UBInt8()
    pad = basic_types.UBInt8Array(length=3)
    name = basic_types.Char(length=base.OFP_MAX_TABLE_NAME_LEN)
    wildcards = basic_types.UBInt32()
    max_entries = basic_types.UBInt32()
    active_count = basic_types.UBInt32()
    count_lookup = basic_types.UBInt64()
    count_matched = basic_types.UBInt64()

    def __init__(self, table_id=None, pad=None, name=None, wildcards=None,
                 max_entries=None, active_count=None, count_lookup=None,
                 count_matched=None):

        self.table_id = table_id
        self.pad = pad
        self.name = name
        self.wildcards = wildcards
        self.max_entries = max_entries
        self.active_count = active_count
        self.count_lookup = count_lookup
        self.count_matched = count_matched
