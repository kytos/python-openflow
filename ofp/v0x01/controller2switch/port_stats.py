"""Body of the port stats reply"""

# System imports

# Third-party imports

# Local source tree imports
from ofp.v0x01.foundation import base
from ofp.v0x01.foundation import basic_types

# Classes


class PortStats(base.GenericStruct):
    """
    Body of reply to OFPST_PORT request. If a counter is unsupported, set
    the field to all ones

        :param port_no:      Port number
        :param pad:          Align to 64-bits
        :param rx_packets:   Number of received packets
        :param tx_packets:   Number of transmitted packets
        :param rx_bytes:     Number of received bytes
        :param tx_bytes:     Number of transmitted bytes
        :param rx_dropped:   Number of packets dropped by RX
        :param tx_dropped:   Number of packets dropped by TX
        :param rx_errors:    Number of receive errors.  This is a super-set
                             of more specific receive errors and should be
                             greater than or equal to the sum of all
                             rx_*_err values
        :param tx_errors:    Number of transmit errors.  This is a super-set
                             of more specific transmit errors and should be
                             greater than or equal to the sum of all
                             tx_*_err values (none currently defined.)
        :param rx_frame_err: Number of frame alignment errors
        :param rx_over_err:  Number of packets with RX overrun
        :param rx_crc_err:   Number of CRC errors
        :param collisions:   Number of collisions
    """
    port_no = basic_types.UBInt16()
    pad = basic_types.UBInt8Array(length=6)
    rx_packets = basic_types.UBInt64()
    tx_packets = basic_types.UBInt64()
    rx_bytes = basic_types.UBInt64()
    tx_bytes = basic_types.UBInt64()
    rx_dropped = basic_types.UBInt64()
    tx_dropped = basic_types.UBInt64()
    rx_errors = basic_types.UBInt64()
    tx_errors = basic_types.UBInt64()
    rx_frame_err = basic_types.UBInt64()
    rx_over_err = basic_types.UBInt64()
    rx_crc_err = basic_types.UBInt64()
    collisions = basic_types.UBInt64()

    def __init__(self, port_no=None, pad=None, rx_packets=None,
                 tx_packets=None, rx_bytes=None, tx_bytes=None,
                 rx_dropped=None, tx_dropped=None, rx_errors=None,
                 tx_errors=None, rx_frame_err=None, rx_over_err=None,
                 rx_crc_err=None, collisions=None):

        self.port_no = port_no
        self.pad = pad
        self.rx_packets = rx_packets
        self.tx_packets = tx_packets
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes
        self.rx_dropped = rx_dropped
        self.tx_dropped = tx_dropped
        self.rx_errors = rx_errors
        self.tx_errors = tx_errors
        self.rx_frame_err = rx_frame_err
        self.rx_over_err = rx_over_err
        self.rx_crc_err = rx_crc_err
        self.collisions = collisions
