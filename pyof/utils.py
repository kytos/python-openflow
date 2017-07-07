"""General Unpack utils for python-openflow."""
import pyof.v0x01.common.header
import pyof.v0x01.common.utils
import pyof.v0x04.common.header
import pyof.v0x04.common.utils
from pyof.foundation.exceptions import UnpackException

pyof_version_libs = {0x01: pyof.v0x01,
                     0x04: pyof.v0x04}


def unpack(packet):
    """Unpack the OpenFlow Packet and returns a message."""
    try:
        version = packet[0]
    except IndexError:
        raise UnpackException('null packet')

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
            if len(binary_data) == header.length - 8:
                message.unpack(binary_data)
            else:
                raise UnpackException(
                    'packet size does not match packet length field')
        return message
    except (UnpackException, ValueError) as e:
        raise UnpackException(e)
