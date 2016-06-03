"""Information about the switch manufactures"""

# System imports

# Third-party imports

# Local source tree imports
from pyof.v0x01.foundation import base
from pyof.v0x01.foundation import basic_types

# Classes


class DescStats(base.GenericStruct):
    """
    Information about the switch manufacturer, hardware revision, software
    revision, serial number, and a description field is avail- able from
    the OFPST_DESC stats request.

        :param mfr_desc:   Manufacturer description
        :param hw_desc:    Hardware description
        :param sw_desc:    Software description
        :param serial_num: Serial number
        :param dp_desc:    Human readable description of datapath
    """
    mfr_desc = basic_types.Char(length=base.DESC_STR_LEN)
    hw_desc = basic_types.Char(length=base.DESC_STR_LEN)
    sw_desc = basic_types.Char(length=base.DESC_STR_LEN)
    serial_num = basic_types.Char(length=base.SERIAL_NUM_LEN)
    dp_desc = basic_types.Char(length=base.DESC_STR_LEN)

    def __init__(self, mfr_desc=None, hw_desc=None, sw_desc=None,
                 serial_num=None, dp_desc=None):

        self.mfr_desc = mfr_desc
        self.hw_desc = hw_desc
        self.sw_desc = sw_desc
        self.serial_num = serial_num
        self.dp_desc = dp_desc
