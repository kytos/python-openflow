"""General Unpack utils for python-openflow."""
import pyof.v0x01.common.header
import pyof.v0x01.common.utils
import pyof.v0x04.common.header
import pyof.v0x04.common.utils
from pyof.foundation.exceptions import UnpackException

pyof_version_libs = {0x01: pyof.v0x01,
                     0x04: pyof.v0x04}


def validate_packet(packet):
    """Check if packet is valid OF packet."""
    if not isinstance(packet, bytes):
        raise UnpackException('invalid packet')

    packet_length = len(packet)

    if packet_length < 8 or packet_length > 2**16:
        raise UnpackException('invalid packet')

    if packet_length != int.from_bytes(packet[2:4],
                                       byteorder='big'):
        raise UnpackException('invalid packet')

    version = packet[0]
    if version == 0 or version >= 128:
        raise UnpackException('invalid packet')


def unpack(packet):
    """Unpack the OpenFlow Packet and returns a message."""
    validate_packet(packet)

    version = packet[0]
    try:
        pyof_lib = pyof_version_libs[version]
    except KeyError:
        raise UnpackException('Version not supported')

    try:
        header = pyof_lib.common.header.Header()
        header.unpack(packet[:8])
        message = pyof_lib.common.utils.new_message_from_header(header)
        binary_data = packet[8:]
        if binary_data:
            message.unpack(binary_data)
        return message
    except (UnpackException, ValueError) as e:
        raise UnpackException(e)
